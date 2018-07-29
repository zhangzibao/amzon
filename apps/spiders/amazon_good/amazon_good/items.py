# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy_djangoitem import DjangoItem

from spiders.models import  small_kind, big_kind, tiny_kind, goods


class bigItem(DjangoItem):
    django_model = big_kind


class smallItem(DjangoItem):
    django_model = small_kind


class tinyItem(DjangoItem):
    django_model = tiny_kind


class goodsItem(DjangoItem):
    django_model = goods

