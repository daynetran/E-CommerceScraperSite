import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from ..items import ProductItem

rank = 1
class BestSellerSpider(CrawlSpider):
    name = 'bestsellers'

    """This spider will take the the category page of Best Sellers and parse it for URLs of the two pages (1-50, 51-100
    ). Then, for each product page, we will find the urls to to each product For each url, we will parse the product 
    page for our desired information. This means three levels of crawling, the best-selling page, then the two product 
    pages, and then the products' individual pages."""


    # start_urls is the link that the Scrapy Spider is fed. In this case, the spider starts with the first page
    # (rank 1-50) of the best sellers list. Then it will run through the second page and collect the product links
    # of the rank 51-100 products.
    start_urls = [
        "https://www.amazon.com/Best-Sellers-Home-Improvement-Power-Core-Drills/zgbs/hi/552800/ref=zg_bs_nav_hi_5_9022404011"
    ]

    def parse(self, response):
        """parse is a built-in function that Scrapy spiders require in order to sort through the page."""

        # Retrieves the page urls from the best-selling page.
        first_page = response.css("ul.a-pagination li.a-selected").css("::attr(href)").extract()
        second_page = response.css("ul.a-pagination li.a-normal").css("::attr(href)").extract()
        # For each page, we will go to their products' product pages and use follow_product_parse to get the desired
        # product info.
        yield Request(first_page[0], callback=get_1st_page)
        yield Request(second_page[0], callback=get_2nd_page)


def get_1st_page(response):
    all_urls = response.css('.zg-item > a::attr(href)').extract()
    for index, url in enumerate(all_urls):
        yield response.follow("http://amazon.com" + url, callback=follow_product_parse, meta={'index': index + 1})
    # for index, url in enumerate(all_urls):
    #     yield Request("http://amazon.com" + url, callback=follow_product_parse, priority=100 - index)


def get_2nd_page(response):
    all_urls = response.css('.zg-item > a::attr(href)').extract()
    for index, url in enumerate(all_urls):
        yield response.follow("http://amazon.com" + url, callback=follow_product_parse, meta={'index': index + 51})
    # for index, url in enumerate(all_urls):
    #     yield Request("http://amazon.com" + url, callback=follow_product_parse, priority=50 - index)


def follow_product_parse(response):
    """This function is applied to every url we find in parse. It gives us the information we want for each product
    from their product pages."""

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
    images = response.css("div#altImages img::attr(src)").extract()
    # XPATH: response.xpath("//*[contains(text(), 'Best Sellers Rank')]") This is here for
    # the search spider, disregard for now.

    # Strips unnecessary blank space from the text
    for i in range(len(name)):
        name[i] = name[i].strip()
    for i in range(len(description)):
        description[i] = description[i].strip()

    # Assigns the retrieved features/variables to our Items.
    if len(name) == 0:
        items['name'] = "Amazon does not have the name. Please click on the product link to see more."
    else:
        items['name'] = name

    if len(name) == 0:
        items['description'] = "The product or Amazon does not have a description. Please click on the link to see " \
                               "more. "
    else:
        items['description'] = description

    if len(price) == 0:
        items['price'] = 'Amazon does not have the price readily available. Please click on the product link to see ' \
                         'more. '
    else:
        items['price'] = price

    if len(name) == 0:
        items['brand'] = "Amazon or the product does not have the brand name. Please click on the product link to see " \
                         "more. "
    else:
        items['brand'] = brand

    if len(name) == 0:
        items['image'] = "Amazon or the product page does not have the image. Please click on the product link to see " \
                         "more. "
    else:
        items['image'] = image

    if len(ratings) == 0:
        items['ratings'] = 'This product does not have any reviews. Please click on the product link to see more.'
    else:
        items['ratings'] = ratings

    if num_reviews is None:
        items['num_reviews'] = '0 ratings'
    else:
        items['num_reviews'] = num_reviews

    items['links'] = links

    if len(images) == 0:
        items['images'] = 'The product has no additional images. Please click on the product link to see more.'
    else:
        items['images'] = images

    global rank
    items['ranks'] = str(response.meta['index'])
    rank += 1

    yield items
