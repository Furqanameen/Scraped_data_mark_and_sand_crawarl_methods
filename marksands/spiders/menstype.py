# -*- coding: utf-8 -*-
import scrapy
# import pandas as pd
from scrapy.http import Request


class MenstypeSpider(scrapy.Spider):
    name = 'menstype'
    allowed_domains = ['marksandspencer.com/c/men']
    start_urls = ['https://www.marksandspencer.com/c/men/']

    def parse(self, response):
        urllink = "https://www.marksandspencer.com"

        for link in response.xpath(".//div[@class='left-navigation']//ul//li//a/@href"):
            fetchlink = urllink + link.extract()
            #print("count links ", fetchlink)
            # yield {"links_geting":fetchlink}
            yield scrapy.Request(fetchlink, self.parse_product_page , dont_filter=True)

        print("tottal link  :", len(fetchlink))

    def parse_product_page(self, response):

        p_link="https://www.marksandspencer.com"
        for product in response.xpath(".//div[@class='product__image product__image--portrait ']/a/@href"):
            fetch_product = p_link+product.extract()
            #yield {"links_geting":fetch_product}
            # print("Product_link",fetch_product)
            yield scrapy.Request(url=fetch_product, callback=self.collectdata , dont_filter=True)

    def collectdata(self, response):
        print("welcome-==========================================")
        collection_title = response.xpath(
                                           ".//div[@class='product-header']/h1/text()").extract_first()
        price = response.xpath("//section/div[@class='clearfix']//p//span[2]//text()").extract_first()
        rev_div=response.xpath(".//div[@class='review-entry__feedback-holder']")

        name=response.xpath(".//div[@class='review-entry__feedback-holder']/h2/text()").extract_first()
        reviews_count=response.xpath(".//section/div//span/strong/text()").extract_first()
        revies_costing=int(reviews_count)

        if revies_costing >0:
            print("Here Extracting Reviews =:")
            Reviews_Loader = response.xpath(".//section/div[@class='clearfix']/div/text()").extract_first()
            coments = response.xpath(".//div[@class='review-entry__name-holder ng-binding']").extract_first()


            yield {"comments are:" :coments,"Rewiesw_Btn":Reviews_Loader}
        else:
            print("Not Yet Any Reviews")

        yield {"title": collection_title,"tottla_reviews":reviews_count,"Price Of Products":price,"name of reviews box":name}
