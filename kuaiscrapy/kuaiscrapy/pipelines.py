# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# import sys
# import os
# sys.path.append(os.pardir)
import pymysql
from four.models import ImagesUrl


class FourPipeline(object):
    def __init__(self, mysql_url, mysql_port, mysql_db):
        self.mysql_url = mysql_url
        self.mysql_port = mysql_port
        self.mysql_db = mysql_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mysql_url=crawler.settings.get('MYSQL_URI'),
            mysql_port=crawler.settings.get('MYSQL_PORT'),
            mysql_db=crawler.settings.get('MYSQL_DATABASE', 't3')
        )

    def open_spider(self, spider):
        self.client = pymysql.Connect(host=self.mysql_url, port=self.mysql_port, user='root', passwd='124578',
                                      db=self.mysql_db)
        self.client.set_charset('utf8')
        self.cursor = self.client.cursor()

    def process_item(self, item, spider):
        if spider.name == 'four':
            title = item['title']
            url = item['movie_url']
            type = item['type']
            second_type = item['second_type']
            cover_url = item['cover_url']
            effect_row_type = self.cursor.execute('select * from four_type WHERE typee LIKE %s', type)
            if not effect_row_type:
                self.cursor.execute('insert into four_type(typee) VALUE (%s)', type)
                type_id = self.client.insert_id()
            else:
                type_id = self.cursor.fetchone()[0]

            effect_row_image = self.cursor.execute('select * from four_imagesurl WHERE images_url LIKE %s', cover_url)
            if not effect_row_image:
                self.cursor.execute('insert into four_imagesurl(images_url) VALUE (%s)', cover_url)
                images_url_id = self.client.insert_id()
            else:
                images_url_id = self.cursor.fetchone()[0]

            effect_row_info = self.cursor.execute('select title from four_mvinfo WHERE title LIKE %s', title)
            if not effect_row_info:
                self.cursor.execute(
                    'insert into four_mvinfo(title,url,second_type,cover_url_id,type_id) VALUE (%s, %s, %s, %s, %s)',
                    (title, url, second_type, images_url_id, type_id))
            self.client.commit()
        elif spider.name == 'tencent':
            cover_img = item['cover_url']
            if not ImagesUrl.objects.filter(images_url=cover_img):
                item['cover_url'] = ImagesUrl.objects.create(images_url=cover_img)
                item.save()
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.client.close()
