# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NshkItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    pubdate = scrapy.Field()
    price = scrapy.Field()

class NSSaleItem(scrapy.Item):
    name = scrapy.Field()
    originalPrice = scrapy.Field()
    rate = scrapy.Field()
    finalPrice = scrapy.Field()
    endDate = scrapy.Field()
    language = scrapy.Field()