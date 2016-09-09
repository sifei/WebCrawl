# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EcigforumItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    forum_name = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    username = scrapy.Field()
    userTitle = scrapy.Field()
    time = scrapy.Field()
    userJoinDate = scrapy.Field()
    userLocation = scrapy.Field()
    postID = scrapy.Field()
    threadID = scrapy.Field()
