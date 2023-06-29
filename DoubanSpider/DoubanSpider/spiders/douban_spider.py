
import scrapy
from ..items import DoubanspiderItem
import traceback


class DoubanSpider(scrapy.Spider):

    name = 'douban'
    offset = 0
    start_urls = [f'https://book.douban.com/top250?start={0}']
    # 生成爬取链接
    # start_urls = [f'https://book.douban.com/top250?start={25*i}' for i in range(10)]

    def parse(self, response):
        books = response.xpath('//div[@class="indent"]/table//tr')
        for book in books:
            try:
                # 处理爬取出去，传给pipeline
                item = DoubanspiderItem()
                item['title'] = book.xpath('.//div[@class="pl2"]/a/text()').get()
                item['book_info'] = book.xpath('.//p[@class="pl"]/text()').get().strip()
                item['score'] = book.xpath('.//span[@class="rating_nums"]/text()').get()
                item['description'] = book.xpath('.//span[@class="inq"]/text()').get()
                yield item
            except Exception:
                print(traceback.format_exc())
