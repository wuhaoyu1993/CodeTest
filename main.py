import traceback
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel, constr, condecimal
import psycopg2
import configparser
import os
from datetime import datetime, date

app = FastAPI()

# 允许跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# 定义图书的请求体和返回体
class Book(BaseModel):
    title: constr(max_length=100) = ''
    author: constr(max_length=100) = ''
    publisher: constr(max_length=100) = ''
    publish_time: date = None
    price: condecimal(max_digits=10,decimal_places=2) = None
    score: condecimal(max_digits=5,decimal_places=2) = None
    description: constr(max_length=100) = ''


# 定义用于接收书名的请求体
class BookDeleteRequest(BaseModel):
    title: str

# 定义reponse body
def get_response(code, message, data):
    response = {
        'code': code,
        'message': message,
        'data': data
    }
    return response


# 连接到PostgreSQL数据库
def get_db_connection():
    root_path = os.path.dirname(__file__)
    config_path = os.path.join(root_path, 'config.ini')
    conf = configparser.ConfigParser()
    conf.read(config_path, encoding="utf-8")
    host = conf.get('Database', 'host')
    port = conf.get('Database', 'port')
    database = conf.get('Database', 'database')
    user = conf.get('Database', 'user')
    password = conf.get('Database', 'password')

    conn = psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password)
    return conn


# 获取所有图书数据
@app.get("/book")
def get_books():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM book order by title")
    rows = cursor.fetchall()
    books = []
    for row in rows:
        book = Book(title=row[0], author=row[1], publisher=row[2], publish_time=row[3], price=row[4], score=row[5],
                    description=row[6])
        books.append(book)
    cursor.close()
    conn.close()
    return get_response(200, 'success', books)


# 删除图书
@app.delete("/book")
def delete_book(book_info: BookDeleteRequest):
    conn = get_db_connection()
    cursor = conn.cursor()
    book_name = book_info.title
    if book_name:
        cursor.execute(f"DELETE FROM book WHERE title='{book_name}'")
        conn.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        conn.close()
        if affected_rows == 0:
            raise HTTPException(status_code=404, detail='Book not found')
        return get_response(200, 'success', 'Book deleted successfully')
    raise HTTPException(status_code=400, detail='bookname can not be empty')


# 新增图书
@app.post("/book")
async def create_book(book_info: Book):
    conn = get_db_connection()
    cursor = conn.cursor()
    book_name = book_info.title
    # 查询图书是否存在，存在则返回不能新增
    cursor.execute(f"SELECT * FROM book WHERE title='{book_name}'")
    rows = cursor.fetchall()
    if rows:
        raise HTTPException(status_code=400, detail='book existed')
    # 图书不存在时，生成插入的图书信息
    author = book_info.author
    publisher = book_info.publisher
    publish_time = book_info.publish_time
    if not publish_time:
        publish_time = 'null'
    else:
        publish_time = "'" + publish_time.strftime("%Y-%m-%d") + "'"
    price = book_info.price if book_info.price else 'null'
    score = book_info.score if book_info.score else 'null'
    description = book_info.description
    # 生成sql并执行
    sql = f"Insert INTO book VALUES ('{book_name}', '{author}', '{publisher}', {publish_time}, {price},{score},'{description}')"
    try:
        cursor.execute(sql)
        conn.commit()
        return get_response(200, 'success', 'Book created successfully')
    except psycopg2.DatabaseError as e:
        print(traceback.format_exc())
        conn.rollback()
        raise HTTPException(status_code=500, detail='internal server error')


# 修改图书
@app.put("/book")
def update_book(book_info: Book):
    # 查询图书，如果图书不存在则返回400
    conn = get_db_connection()
    cursor = conn.cursor()
    book_name = book_info.title
    cursor.execute(f"SELECT * FROM book WHERE title='{book_name}'")
    rows = cursor.fetchall()
    if not rows:
        raise HTTPException(status_code=404, detail='book not existed')
    # 图书存在的情况下，根据传入参数和已有数据，组成sql
    rows = rows[0]
    author = book_info.author if book_info.author else rows[1]
    author = author if author else ''
    publisher = book_info.publisher if book_info.publisher else rows[2]
    publisher = publisher if publisher else ''
    publish_time = book_info.publish_time
    if not publish_time:
        if rows[3]:
            publish_time = "'" + str(rows[3]) + "'"
        else:
            publish_time = 'null'
    price = book_info.price if book_info.price else rows[4]
    price = price if price else 'null'
    score = book_info.score if book_info.score else rows[5]
    score = score if score else 'null'
    description = book_info.description if book_info.description else rows[6]
    description = description if description else ''
    # 执行sql语句
    sql = f"""UPDATE book SET 
    author='{author}', publisher ='{publisher}', publish_time={publish_time}, price={price}, score={score}, description='{description}' 
    WHERE title='{book_name}'
    """
    try:
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
        return get_response(200, 'success', 'Book updated successfully')
    except psycopg2.DatabaseError as e:
        print(traceback.format_exc())
        conn.rollback()
        raise HTTPException(status_code=500, detail='internal server error')


if __name__ == '__main__':
    uvicorn.run(app=app)
