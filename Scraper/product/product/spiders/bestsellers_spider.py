from ..items import BestSellersItem
import scrapy

first_urls = dict()
second_urls = dict()


# x = input('Please enter Amazon bestselling url here: ')
# y = input('Please enter the name of the csv: ____.csv ')

class BestSellerSpider(scrapy.Spider):
    name = 'bestsellers'

    # custom_settings = {
    #     "FEED_FORMAT": "csv",
    #     "FEED_URI": "{}.csv".format(y)
    # }

    """This spider will take the the category page of Amazon's Best Sellers and parse it for URLs of the two bestselling pages (1-50, 51-100
    ). Then, for each product page, we will find the urls to to each product For each url, we will parse the product
    page for our desired information. This means three levels of crawling, the best-selling page, then the two product
    pages, and then the products' individual pages."""

    def __init__(self, **kwargs):
        super().__init__()
        self.start_urls = [kwargs.get('start_url')]

    def parse(self, response):
        """parse is a built-in function that Scrapy spiders require in order to sort through the page. We extract the
         links for the bestselling pages on Amazon."""

        # Parses Amazon's bestselling page for the two page urls.
        first_page = response.css('ul.a-pagination li.a-selected').css('a::attr(href)').get()
        second_page = response.css('ul.a-pagination li.a-normal').css('a::attr(href)').get()
        # Retrieves the product urls from the pages by calling get_x_page
        yield response.follow(url=first_page, callback=parse_1st_page)
        yield response.follow(url=second_page, callback=parse_2nd_page)
        # yield response.follow(second_page, callback=parse_2nd_page)


def parse_1st_page(document):
    """get_1st_page is our function that scrapes the product urls of the top 50 products from Amazon's first
    best-selling page. It stores the urls in the first_urls dictionary"""

    urls = document.css("span.zg-item > a.a-link-normal:not(a.a-text-normal)::attr(href)").getall()
    for index, url in enumerate(urls):
        first_urls[index + 1] = url


def parse_2nd_page(document):
    """get_2nd_page is our function that scrapes the product urls of the 51-100 products from Amazon's second
    best-selling page. It stores the urls in the second_urls dictionary, then combines first_urls and second_urls
    into a dictionary called all_urls. Then for each url in all_urls, it goes to the product page and calls
    follow_product_parse."""

    urls = document.css("span.zg-item > a.a-link-normal:not(a.a-text-normal)::attr(href)").getall()
    for index, url in enumerate(urls):
        second_urls[index + 51] = url
    x = first_urls
    all_urls = {**x, **second_urls}
    for index, product_url in enumerate(all_urls.values()):
        yield document.follow("http://amazon.com" + product_url, callback=follow_product_parse,
                              meta={'index': index + 1})


def follow_product_parse(document):
    """This function is applied to every url we find in parse. It gives us the information we want for each product
    from their product pages."""

    # Initializes the Item that will receive the information from the parsing
    items = BestSellersItem()

    # Assigns the various desired features of our product page to corresponding variables
    name = document.css("#productTitle").css("::text").extract()
    if not name:
        name = document.css(".feature_Title ::text").extract()
    if not name:
        name = document.css(".qa-title-text ::text").extract()

    description = document.css("#feature-bullets > ul > li:not(#replacementPartsFitmentBullet)").css(
        '::text').extract()
    if not description:
        description = document.css(".qa-bullet-point-list-element").css("::text").extract()

    price = document.css("#priceblock_saleprice, #priceblock_ourprice").css("::text").extract()
    if not price:
        price = document.css(".qa-price-block-our-price").css("::text").extract()
    if not price:
        price = document.css("#priceblock_dealprice::text").extract()
    if not price:
        price = document.css("#priceblock_pospromoprice::text").extract()

    brand = document.css("#bylineInfo::text").extract()
    if not brand:
        brand = document.css(".qa-byline-url::text").extract()

    rating = document.css("span[data-hook = 'rating-out-of-text']::text").extract()

    num_reviews = document.css("#acrCustomerReviewText::text").extract_first()
    if not num_reviews:
        num_reviews = document.css(".qa-average-customer-rating-review-text::text").extract()

    link = document.css("link[rel = 'canonical']").css("::attr(href)").extract()

    list_price = document.css(".priceBlockStrikePriceString::text").extract_first()

    # Strips unnecessary blank space from the text
    for i in range(len(name)):
        name[i] = name[i].strip()
    for i in range(len(description)):
        description[i] = description[i].strip()

    # Assign values to the Scrapy item
    if name:
        items['name'] = name
    if description:
        items['description'] = description
    if price:
        items['price'] = price
    if brand:
        items['brand'] = brand
    if rating:
        items['rating'] = rating
    if num_reviews:
        items['num_reviews'] = num_reviews
    if link:
        items['link'] = link
    if list_price:
        items['list_price'] = list_price
    items['rank'] = str(document.meta['index'])

    yield items
