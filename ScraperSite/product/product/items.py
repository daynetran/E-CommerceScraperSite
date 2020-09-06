# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BestSellersItem(scrapy.Item):
    rank = scrapy.Field()
    images = scrapy.Field()


class ProductItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
    brand = scrapy.Field()
    # image = scrapy.Field()
    # images = scrapy.Field()
    rating = scrapy.Field()
    num_reviews = scrapy.Field()
    link = scrapy.Field()
    rank = scrapy.Field()
    list_price = scrapy.Field()
    #manufacturer
    #days til product arrives
    #product rating, number of reviews
    #Product Description ***

    pass
