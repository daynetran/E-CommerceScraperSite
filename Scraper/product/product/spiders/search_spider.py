import scrapy
from scrapy.spiders import CrawlSpider
from ..items import BestSellersItem

x = 1


class SearchSpider(CrawlSpider):
    name = 'search'
    start_urls = ['https://www.amazon.com/s?k=bottle+jack&ref=nb_sb_noss_2']

    def parse(self, response):
        urls = response.css(".a-size-medium::attr(href)")
        for index, url in enumerate(urls):
            yield response.follow("http://amazon.com" + url, callback=follow_product_parse, meta={'index': index + x})


def follow_product_parse(response):
    # Initializes the Item that will receive the information from the parsing
    items = ProductItem()
    # Assigns the various desired features of our product page to corresponding variables
    name = response.css("#productTitle::text").extract()
    description = response.css("#feature-bullets > ul > li:not(#replacementPartsFitmentBullet)").css(
        '::text').extract()
    price = response.css("#priceblock_saleprice, #priceblock_ourprice").css("::text").extract()
    brand = response.css("#bylineInfo::text").extract()
    image = response.css("#landingImage::attr(src)").extract()
    ratings = response.css("span[data-hook = 'rating-out-of-text']::text").extract()
    num_reviews = response.css("#acrCustomerReviewText::text").extract_first()
    links = response.css("link[rel = 'canonical']").css("::attr(href)").extract()
    # ranks = response.css("#productDetails_detailBullets_sections1 > tr:nth_child(8) > td > span >
    # span::text").extract()
    images = response.css("div#altImages img::attr(src)").extract()
    # XPATH: response.xpath("//*[contains(text(), 'Best Sellers Rank')]")

    # Strips unnecessary blank space from the text
    x = str(response.meta['index'])
    for i in range(len(name)):
        name[i] = name[i].strip()
    for i in range(len(description)):
        description[i] = description[i].strip()

    # Assigns the desired/retrieved features/variables to our Items.
    items['name'] = name
    items['description'] = description
    if len(price) == 0:
        items[
            'price'] = 'Amazon does not have the price readily available. Please click on the product link to see more.'
    else:
        items['price'] = price
    items['brand'] = brand
    items['image'] = image
    if len(ratings) == 0:
        items['ratings'] = 'This product does not have any reviews.'
    else:
        items['ratings'] = ratings
    items['num_reviews'] = num_reviews
    items['links'] = links
    items['ranks'] = x
    if len(images) == 0:
        items['images'] = 'The product has no additional images'
    else:
        items['images'] = images
        yield items
