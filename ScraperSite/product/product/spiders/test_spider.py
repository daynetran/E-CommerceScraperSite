# -*- coding: utf-8 -*-
import scrapy
from ..items import ProductItem

rank = 0


class TestSpider(scrapy.Spider):
    """This TestSpider is designed to test product page parsing on a small scale. Rather than test the 100
    bestselling products or x many search products all at once, we can test our product-parsing abilities on just
    these two keyboard products """

    name = 'test'
    start_urls = ['https://www.amazon.com/Arteck-Wireless-Keyboard-Stainless-Rechargeable/dp/B07D34L57F/ref=sr_1_2'
                  '?dchild=1/', "https://www.amazon.com/Apple-Keyboard-Wireless-Rechargable-English/dp/B016QO64FI/ref"
                                "=zg_bs_12879431_4?_encoding=UTF8&psc=1&refRID=7M1A3S6CJBP7C0F973XH"]

    def parse(self, response):

        # Initializes the Item that will receive the information from the parsing
        items = ProductItem()

        # Assigns the various desired features of our product page to corresponding variables
        # If you want to test how you select the features with CSS, use this command in the terminal:
        # scrapy shell url_link (here put the actual url)
        # this will let you test various response.css("x").extract()'s to make sure you pull info correctly
        name = response.css("#productTitle::text").extract()
        description = response.css("#feature-bullets > ul > li:not(#replacementPartsFitmentBullet)").css('::text'). \
            extract()
        price = response.css("#priceblock_saleprice, #priceblock_ourprice").css("::text").extract()
        brand = response.css("#bylineInfo::text").extract()
        image = response.css("#landingImage::attr(src)").extract()
        num_reviews = response.css("#acrCustomerReviewText::text").extract_first()
        ratings = response.css("span[data-hook = 'rating-out-of-text']::text").extract()
        global rank
        rank += 1
        x = str(rank)
        # Strips unnecessary blank space from the text
        for i in range(len(name)):
            name[i] = name[i].strip()
        for i in range(len(description)):
            description[i] = description[i].strip()

        # Assigns the desired features/variables to our Items.
        items['name'] = name
        items['description'] = description
        if len(price) == 0:
            items[
                'price'] = 'Amazon does not have the price readily available. Please click on the product link to' \
                           ' see more. '
        else:
            items['price'] = price
        items['brand'] = brand
        items['image'] = image
        items['ratings'] = ratings
        items['num_reviews'] = num_reviews
        items['ranks'] = x

        yield items
