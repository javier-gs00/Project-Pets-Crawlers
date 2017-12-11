# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProjectPetsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    href = scrapy.Field()
    image_href = scrapy.Field()
    category = scrapy.Field()
    animal = scrapy.Field()
    store = scrapy.Field()
    date = scrapy.Field()
    date_str = scrapy.Field()