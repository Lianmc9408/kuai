# -*- coding: utf-8 -*-
import json

import scrapy

# from four.kuaiscrapy import items


from ..items import TencentNewsItem


class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['qq.com']
    start_urls = ['http://ent.qq.com/']

    base_url = 'http://openapi.inews.qq.com/getQQNewsNormalContent?id={id}&refer=mobilewwwqqcom'

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.list_parse)

    def list_parse(self, response):
        articals = response.xpath('.//div[@class="Q-tpList"]')
        for artical in articals:
            # cover_url = artical.xpath('.//a//img[@class="picto"]/@src').extract_first()
            # title = artical.xpath('.//div[@class="text"]//a[@class="linkto"]/text()').extract_first()
            detail_url = artical.xpath('.//div[@class="text"]//a[@class="linkto"]/@href').extract_first()
            id = detail_url.split('/')[-1].split('.')[0]+'00'
            # print('detail-----', id)
            yield scrapy.Request(self.base_url.format(id=id), callback=self.detail_parse)
    # http://openapi.inews.qq.com/getQQNewsNormalContent?id = 20171214A0IVVN00&refer=mobilewwwqqcom
    def detail_parse(self, response):
        content = json.loads(response.text, encoding='utf8')
        if content:
            title = content['title']
            cover_img = content['img']['imgurl']
            id = content['id']
            artical = content['content']
            # print(title, cover_img, id, artical)
            # item = items.TencentNewsItem()
            item = TencentNewsItem()
            item['a_id'] = id
            item['title'] = title
            item['cover_url'] = cover_img
            item['artical'] = artical
            yield item
        # print(content)