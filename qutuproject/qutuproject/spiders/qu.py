# -*- coding: utf-8 -*-
import scrapy
from qutuproject.items import QutuprojectItem
import os

class QuSpider(scrapy.Spider):
    name = 'qu'
    allowed_domains = ['www.gushiking.com']
    start_urls = ['http://www.gushiking.com/gaoxiao/index.htm']

    url = 'http://www.gushiking.com/gaoxiao/index_p{}.htm'
    page = 1

    def parse(self, response):
        # 先找到所有的div
        div_list = response.xpath('//div[@id="container"]/div[@class="left"]/div')[:-1]
        for odiv in div_list:
            item = QutuprojectItem()
            # 图片标题
            item['name'] = odiv.xpath('./div[@class="pic"]//img/@alt').extract_first()
            # 图片链接
            item['image_url'] = odiv.xpath('./div[@class="pic"]//img/@src').extract_first()
            yield item

            yield scrapy.Request(url=item['image_url'], callback=self.download)

        if self.page <= 5:
            self.page += 1
            url = self.url.format(self.page)
            yield scrapy.Request(url, callback=self.parse)

    # 下载图片的函数，referer会自动添加
    def download(self, response):
        dirpath = r'C:\Users\ZBLi\Desktop\1801\day09\qutu'
        # 获取请求的url
        image_url = response.url
        # 获取图片的名字
        image_name = os.path.basename(image_url)
        # 获取图片的路径
        image_path = os.path.join(dirpath, image_name)
        # 下载图片
        with open(image_path, 'wb') as fp:
            fp.write(response.body)
