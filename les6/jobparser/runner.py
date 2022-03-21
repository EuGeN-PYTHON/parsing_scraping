import threading

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from jobparser import settings
from jobparser.spiders.hhru import HhruSpider
from jobparser.spiders.sjru import SjruSpider

if __name__ == '__main__':
    settings_crawler = Settings()
    settings_crawler.setmodule(settings)

    crawler_process = CrawlerProcess(settings=settings_crawler)

    crawler_process.crawl(HhruSpider)
    crawler_process.crawl(SjruSpider)

    crawler_process.start()

    # Запуск через 2 потока

    # threads = []
    # x = threading.Thread(target=crawler_process.crawl(HhruSpider), args=(1,))
    # threads.append(x)
    # x.start()
    # x = threading.Thread(target=crawler_process.crawl(SjruSpider), args=(2,))
    # for index, thread in enumerate(threads):
    #     thread.join()


