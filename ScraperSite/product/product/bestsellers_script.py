from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from product.product import tableclean

process = CrawlerProcess(get_project_settings())
process.crawl('bestsellers')
process.start()

cleaned = tableclean.clean_table("{}.csv".format("ScrapedData"))
tableclean.create_csv(cleaned)
