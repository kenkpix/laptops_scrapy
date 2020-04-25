# -*- coding: utf-8 -*-
import scrapy
import json


class AmazonLink(scrapy.Spider):
    name = 'amazon_spider'
    allowed_domains = ['https://www.amazon.com/']
    start_urls = ['https://www.amazon.com/s?i=computers&rh=n%3A172282%2Cn%3A493964%2Cn%3A541966%2Cn%3A13896617011%2Cn%3A565108&page=' + str(i) for i in range(1, 401)]

    def parse(self, response):
        for link in response.xpath("//a[@class='a-link-normal a-text-normal']/@href").getall():
            yield {'link': link}


# class AmazonData(scrapy.Spider):
#     name = 'amazon_laptops'
#     allowed_domains = ['https://www.amazon.com/']

#     with open

#     start_urls = []
    