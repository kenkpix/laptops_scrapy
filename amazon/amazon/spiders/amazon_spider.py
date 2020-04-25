# -*- coding: utf-8 -*-
import scrapy
import json
import pandas as pd


class AmazonLink(scrapy.Spider):
    name = 'amazon_spider'
    allowed_domains = ['https://www.amazon.com/']
    start_urls = ['https://www.amazon.com/s?i=computers&rh=n%3A172282%2Cn%3A493964%2Cn%3A541966%2Cn%3A13896617011%2Cn%3A565108&page=' + str(i) for i in range(1, 401)]

    def parse(self, response):
        for link in response.xpath("//a[@class='a-link-normal a-text-normal']/@href").getall():
            yield {'link': link}


class AmazonData(scrapy.Spider):
    name = 'amazon_laptops'
    allowed_domains = ['https://www.amazon.com/']

    with open('/home/vladislav/GitHub/laptops_scrapy/amazon/output.json', 'r') as f:
        links = json.load(f)

    df = pd.DataFrame(links)

    to_drop = ["/electronics-store/b?ie=UTF8&node=172282",
           "/computer-pc-hardware-accessories-add-ons/b?ie=UTF8&node=541966",
           "/Computers-Tablets/b?ie=UTF8&node=13896617011"]
    
    for link in to_drop:
        df = df.drop(df[df.link == link].index)   

    df = df[~df['link'].str.startswith('https://')]
    df = df.drop_duplicates()
    # # TEMP
    # testing = df.iloc[0:5]
    # # TEMP
    start_urls = ['https://www.amazon.com' + str(i) for i in df.link.values]

    def parse(self, response):
        for vals in response.xpath("(//table[@class='a-keyvalue prodDetTable'])[1]"):
            yield {
                'values': vals.xpath("//td[@class='a-size-base']/text()").getall(),
            }



    