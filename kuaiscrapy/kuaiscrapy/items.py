# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FourItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    movie_url = scrapy.Field()
    type = scrapy.Field()
    second_type = scrapy.Field()
    cover_url = scrapy.Field()
