import psycopg2
import configparser
import os

class Book():

    def __init__(self):
        root_path = os.path.dirname(os.path.dirname(__file__))
        config_path = os.path.join(root_path, 'config.ini')
        conf = configparser.ConfigParser()
        conf.read(config_path, encoding="utf-8")
        host = conf.get('Database', 'host')
        port = conf.get('Database', 'port')
        database = conf.get('Database', 'database')
        user = conf.get('Database', 'user')
        password = conf.get('Database', 'password')

        self.conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password)

    def create_database(self):
        cursor = self.conn.cursor()
        sql = """
        create table book (
            title VARCHAR(100) not NULL PRIMARY KEY,
            author VARCHAR(100),
            publisher VARCHAR(100),
            publish_time date,
            price DECIMAL(10,2),
            score DECIMAL(5,2),
            description VARCHAR(100)
            ) 
        """
        cursor.execute(sql)
        cursor.close()
        self.conn.commit()
        self.conn.close()


if __name__ == '__main__':

    book_database = Book()
    book_database.create_database()


