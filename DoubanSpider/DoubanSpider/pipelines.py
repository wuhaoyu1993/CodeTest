# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import re

from itemadapter import ItemAdapter

import psycopg2
import configparser
import os
import time


class DoubanspiderPipeline:

    def __init__(self):
        # 初始化这个pipeline时读取数据库配置
        root_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        config_path = os.path.join(root_path, 'config.ini')
        conf = configparser.ConfigParser()
        conf.read(config_path, encoding="utf-8")
        self.host = conf.get('Database', 'host')
        self.port = conf.get('Database', 'port')
        self.database = conf.get('Database', 'database')
        self.user = conf.get('Database', 'user')
        self.password = conf.get('Database', 'password')

    def open_spider(self, spider):
        # 初始化爬虫时链接数据库
        self.connection = psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password
        )
        self.cursor = self.connection.cursor()

    def close_spider(self, spider):
        # 关闭爬虫时关闭数据库链接
        self.cursor.close()
        self.connection.close()

    def process_item(self, item, spider):
        # 处理书名
        title = item.get('title').strip()
        book_info = item.get('book_info')
        # 处理评分
        socre = item.get('score').strip()
        book_info_list = book_info.split('/')
        book_info_list = [i.strip() for i in book_info_list]
        # 处理某些有两个价格的图书
        if re.match('(\d+\.*\d*元)', book_info_list[-2]):
            book_info_list.remove(book_info_list[-2])
        # 处理某些有多个作者的图书
        if len(book_info_list) > 4:
            author = '/'.join(book_info_list[:-3])
        else:
            author = book_info_list[0].strip()
        # 处理出版社
        publisher = book_info_list[-3].strip()
        # 处理不同格式的日期并转化成同一格式
        publish_time = book_info_list[-2].replace('.', '-').replace('年', '-').replace('月', '-').split('-')
        publish_time = [i.strip() for i in publish_time if i]
        if len(publish_time) == 1:
            publish_time.append('01')
            publish_time.append('01')
        elif len(publish_time) == 2:
            publish_time.append('01')
        publish_time = '-'.join(publish_time)
        # 处理价格并转成浮点数
        price = book_info_list[-1].strip()
        if not price:
            price = '0'
        else:
            price = re.search('(\d+\.*\d*)', price).group(1)
        # 处理图书描述
        description = item.get('description')
        if description:
            description = description.strip()
        else:
            description = ''
        # 构造sql
        sql = f"""
        Insert INTO book VALUES ('{title}', '{author}', '{publisher}', '{publish_time}', '{price}','{socre}','{description}')
        ON conflict(title) DO update set
        author = '{author}',publisher = '{publisher}',publish_time = '{publish_time}',price = '{price}',score = '{socre}',description = '{description}'
        """
        # 执行sql
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except psycopg2.DatabaseError as e:
            self.connection.rollback()
            raise e
        return item
