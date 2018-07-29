# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
from spiders.models import ProxyIp

class ProxyipDjangoItem(DjangoItem):
    # define the fields for your item here like:
    # name = scrapy.Field()
    django_model = ProxyIp

class ProxyipItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

