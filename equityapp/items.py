# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class EquityappItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = Field()
    address = Field()
    building = Field()
    floor_plan = Field()
    bedroom = Field()
    bathroom = Field()
    size = Field()
    price = Field()
    length = Field()
    move_in = Field()
    description = Field()
    latitude = Field()
    longitude = Field()
    pictures = Field()
    source = Field()
    url = Field()
