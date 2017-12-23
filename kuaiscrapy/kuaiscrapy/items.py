# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from four.models import Artical
from scrapy_djangoitem import DjangoItem

class FourItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    movie_url = scrapy.Field()
    type = scrapy.Field()
    second_type = scrapy.Field()
    cover_url = scrapy.Field()

# class ImagesUrl(models.Model):
#     images_url = models.CharField(max_length=255, unique=True)
#
# class Artical(models.Model):
#     a_id = models.CharField(max_length=32, unique=True)
#     title = models.CharField(max_length=128)
#     artical = models.TextField()
#     cover_url = models.ForeignKey(to='ImagesUrl', on_delete=models.CASCADE)

# class TencentNewsItem(DjangoItem):
#     title = scrapy.Field()
#     id = scrapy.Field()
#     artical = scrapy.Field()
#     cover_url = scrapy.Field()


class TencentNewsItem(DjangoItem):
    django_model = Artical