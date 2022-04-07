# from scrapy.crawler import CrawlerRunner
# from scrapy.utils.log import configure_logging
# from twisted.internet import reactor
# from scrapy.utils.project import get_project_settings
from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess

from stroyparser import settings
from stroyparser.spiders.lmru import LmruSpider

if __name__ == '__main__':
    search_word = 'стол'
    settings_crawler = Settings()
    settings_crawler.setmodule(settings)

    crawler_process = CrawlerProcess(settings=settings_crawler)

    crawler_process.crawl(LmruSpider, keyword=search_word)

    crawler_process.start()


    # Запуск через 2 потока

    # threads = []
    # x = threading.Thread(target=crawler_process.crawl(HhruSpider), args=(1,))
    # threads.append(x)
    # x.start()
    # x = threading.Thread(target=crawler_process.crawl(SjruSpider), args=(2,))
    # threads.append(x)
    # x.start()
    # for index, thread in enumerate(threads):
    #     thread.join()


