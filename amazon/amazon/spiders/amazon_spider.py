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

    with open('D:/github/laptops_scrapy/amazon/output.json', 'r') as f:
        links = json.load(f)

    df = pd.DataFrame(links)

    to_drop = ["/electronics-store/b?ie=UTF8&node=172282",
           "/computer-pc-hardware-accessories-add-ons/b?ie=UTF8&node=541966",
           "/Computers-Tablets/b?ie=UTF8&node=13896617011"]
    
    for link in to_drop:
        df = df.drop(df[df.link == link].index)   

    df = df[~df['link'].str.startswith('https://')]
    df = df.drop_duplicates()

    start_urls = ['https://www.amazon.com' + str(i) for i in df.link.values]

    table_section_1 = pd.DataFrame(columns=[
        'Screen Size', 'Screen Resolution', 'Max Screen Resolution',
        'Processor', 'RAM', 'Memory Speed', 'Chipset Brand',
        'Card Description', 'Graphics Card Ram Size', 'Wireless Type',
        'Number of USB 2.0 Ports', 'Number of USB 3.0 Ports',
        'Hard Drive', 'Graphics Coprocessor', 'Price', 'URL'])
    
    table_section_2 = pd.DataFrame(columns=[
        'Brand Name', 'Series', 'Item Model number',
        'Hardware Platform', 'Operating System', 'Item Weight',
        'Product Dimensions', 'Processor Brand','Processor Count', 
        'Batteries', 'Computer Memory Type', 'Hard Drive Rotational Speed', 
        'Power Source', 'URL'
    ])

    def parse(self, response):
        product = response.url.split("/")[-1]

        section_1_path = response.xpath("//table[@id='productDetails_techSpec_section_1']//tr")
        keys_1 = [x.strip() for x in section_1_path.xpath(".//th/text()").getall()]
        values_1 = [x.strip() for x in section_1_path.xpath(".//td/text()").getall()]

        section_1_dict = dict(zip(keys_1, values_1))
        section_1_dict.update({'URL': response.url})
        price = [x.strip() for x in response.xpath("//span[@id='priceblock_ourprice']/text()").getall()]
        if len(price) != 0:
            section_1_dict.update({'Price': price[0]})
        else:
            section_1_dict.update({'Price': None})

        for key, val in section_1_dict.items():
            if key in list(self.table_section_1):
                self.table_section_1.loc[product, key] = val

        section_2_path = response.xpath("//table[@id='productDetails_techSpec_section_2']//tr")
        keys_2 = [x.strip() for x in section_2_path.xpath(".//th/text()").getall()]
        values_2 = [x.strip() for x in section_2_path.xpath(".//td/text()").getall()]

        section_2_dict = dict(zip(keys_2, values_2))
        section_2_dict.update({'URL': response.url})

        for key2, val2 in section_2_dict.items():
            if key2 in list(self.table_section_2):
                self.table_section_2.loc[product, key2] = val2

        result_file = self.table_section_1.merge(self.table_section_2).to_csv('Amazon_Laptops_data.csv')
