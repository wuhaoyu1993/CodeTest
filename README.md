# Python Code Test

环境要求
=
    Python 3.11
    PostgreSQL15.3

安装
=
 1.克隆仓库：

    git clone https://github.com/your-username/douban-spider.git
2.进入项目目录：

    cd CodeTest
3.安装所需的 Python 包：

    pip install -r requirements.txt
4.在config.ini文件里配置数据库链接

5.生成需要的数据表

    cd models
    python book.py

使用方法
=
1.回到根目录，运行爬虫
    
    cd ..
    cd DoubanSpider
    scrapy crawl douban

2.回到根目录，启动后台服务器
    
    cd ..
    python main.py

3.双击index.html，用浏览器打开

页面功能
=
1.查询功能：点击search按钮，查询当前爬取的所有图书信息

2.新增功能：在Add Book下的输入框里输入图书信息然后点击Add按钮，可以在数据库里插入一条新的图书

3.更新功能：在Add Book下的输入框里输入图书信息然后点击Update按钮，可以更新一本已经在数据库的书籍

4.删除功能：点击Books下列表里的Delete按钮，删除数据库里的一条书籍数据

贡献
=
欢迎贡献！请先 fork 本仓库，然后提交拉取请求。