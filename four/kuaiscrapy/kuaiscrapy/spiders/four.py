# -*- coding: utf-8 -*-
import scrapy

# from four.kuaiscrapy import items
from ..items import FourItem

class FourSpider(scrapy.Spider):
    name = 'four'
    allowed_domains = ['1191v.com']
    start_urls = ['https://www.1191v.com']

    url = 'https://www.1191v.com/'

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.page_parse)


    def page_parse(self, response):
        # av_best = response.xpath('//div[@class=title]/a/@href').extract_first()
        menu_list = response.css('.wrap .movie_list .title a::attr(href)').extract()
        for menu in menu_list:
            url = response.urljoin(menu)
            yield scrapy.Request(url=url, callback=self.list_page_parse)

    def list_page_parse(self, response):
        type = response.css('.wrap .cat_pos a[href^="/Html"]::text').extract_first()
        av_list = response.css('.movie_list li a::attr(href)').extract()

        for av_url in av_list:
            av_url = response.urljoin(av_url)
            yield scrapy.Request(url=av_url, callback=self.detail_parse, meta={'type': type})
        next_page_url = response.css('.pagination a[class="next pagegbk"]').re_first('.*?href="(.*?)" cla.*?下一页')
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(next_page_url, callback=self.list_page_parse)

    def detail_parse(self, response):
        title = response.css('.film_info .film_title  h1::text').extract_first()
        cover_url = response.css('.film_info dd span a').re_first('.*?href="(.*?)" target.*?图片下载')
        # movie_url = response.css('.film_bar .jishu .con4 .downurl a::attr(href)').extract_first()
        movie_url = response.css('.downurl > a:nth-child(1)::attr(href)').extract_first()
        # second_type = response.css('.film_bar dd').re_first(r'\s*情色分類：\s*<span>(.*?)</span>')
        second_type = response.css('.movie_info > dl:nth-child(1) > dd:nth-child(5) > span:nth-child(1)::text').extract_first()
        type = response.meta['type']
        # item = items.FourItem()
        item = FourItem()
        item['title'] = title
        item['type'] = type
        item['movie_url'] = movie_url
        item['cover_url'] = cover_url
        item['second_type'] = second_type
        yield item
        # print(type, second_type, title, cover_url, movie_url)
        # https://www.5120t.com/Html/100/23236.html