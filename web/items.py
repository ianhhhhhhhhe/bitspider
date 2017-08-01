# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WebItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    time = scrapy.Field()
    tag = scrapy.Field()
    photo = scrapy.Field()
    lang = scrapy.Field()