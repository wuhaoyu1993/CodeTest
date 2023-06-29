import os

if __name__ == '__main__':

    path = os.path.dirname(__file__)
    path = os.path.join(path, 'DoubanSpider')
    path = os.path.join(path, 'spiders')
    path = os.path.join(path, 'douban_spider.py')
    os.system(f'scrapy runspider {path}')