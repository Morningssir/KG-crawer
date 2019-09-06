# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PatentCrawerItem(scrapy.Item):
    # define the fields for your item here like:
    # name
    nm = scrapy.Field()
    # id
    id = scrapy.Field()
    # date
    dt = scrapy.Field()
    # developer
    dp = scrapy.Field()
    # summary
    su = scrapy.Field()
    # relation
    rl = scrapy.Field()

