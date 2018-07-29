import scrapy
import re
from decimal import *
from scrapy.http.request import Request
from spiders.models import amazon_goods


def filter_url(url):
    pattern = re.compile("\/ref=[^/]*[\/?]")
    default = re.findall(pattern, url)
    if default:
        default = default[0]
        default = default.replace('/ref=', '')
        default = default.replace('?', '')
        url = url.replace(default, 'cbw_direct_from_1')
    return url


def good_save(response):
    if len(response.xpath(".//span[@id='priceblock_ourprice']/text()")) > 0:
        name = response.xpath(".//span[@id='productTitle']/text()").extract()[0].strip()
        price = response.xpath(".//span[@id='priceblock_ourprice']/text()").extract()[0].strip()
        img = response.xpath(".//img[@id='landingImage']/@data-a-dynamic-image").extract()[0].strip()
        pattern = re.compile("https[^\"]*")
        default = re.findall(pattern, img)
        if default:
            img = default[0]
        try:
            good = amazon_goods.objects.get(name=name)
        except amazon_goods.DoesNotExist:
            # 捕获City不存在的异常, 抛出异常或是自己处理
            good = amazon_goods()
        good.name = name
        good.price = price.replace("$", '')
        # good.price = 2
        print(price)
        good.imgurl = img
        good.url = response.url
        good.save()
    else:
        print("no sense:", response.url)


class amazon_good(scrapy.Spider):
    name = 'amazon_good'
    allowed_domains = ["www.amazon.com"]
    start_urls = 'https://www.amazon.com/gp/site-directory/ref=nav_shopall_btn'
    base_url = 'https://www.amazon.com'
    urls = []

    def start_requests(self):
        with open('./urls.txt', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                self.urls.append(line.strip('\n'))

        for url in self.urls:
            url = filter_url(url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        ul = response.xpath(
            ".//ul[@class='a-unordered-list a-nostyle a-button-list a-declarative a-button-toggle-group a-horizontal a-spacing-top-micro swatches swatchesSquare imageSwatches']")
        li_s = ul.xpath(".//li")
        if (len(li_s) > 0):
            for li in li_s:
                url = li.xpath("@data-dp-url").extract()[0].strip()
                defaults = li.xpath("@data-defaultasin").extract()[0].strip()
                if len(url) == 0:
                    print(defaults)
                    pattern = re.compile("\/B[^/]*[\/?]")
                    default = re.findall(pattern, response.url)[0]
                    default = default.replace('/', '')
                    default = default.replace('?', '')
                    url = response.url.replace(default, defaults)
                    print(url)
                else:
                    url = '{}/{}'.format(amazon_good.base_url, url)
                    # 二次过滤
                    url = filter_url(url)
                yield scrapy.Request(url=url, callback=self.good_parse, dont_filter=True)
        else:
            good_save(response)

    def good_parse(self, response):
        good_save(response)
