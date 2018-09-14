# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import re

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose




# class WeiboItemLoader(ItemLoader):
#     #自定义itemloader
#     default_output_processor = TakeFirst()

class WeiboluhanItem(scrapy.Item):
    # define the fields for your item here like:
    comment = scrapy.Field()
    pass
