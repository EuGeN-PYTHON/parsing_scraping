from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess

from instagramparser import settings
from instagramparser.spiders.InstagramSpider import InstagramspiderSpider

if __name__ == '__main__':

    settings_crawler = Settings()
    settings_crawler.setmodule(settings)

    crawler_process = CrawlerProcess(settings=settings_crawler)

    crawler_process.crawl(InstagramspiderSpider)

    crawler_process.start()