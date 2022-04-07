# from scrapy.crawler import CrawlerRunner
# from scrapy.utils.log import configure_logging
# from twisted.internet import reactor
# from scrapy.utils.project import get_project_settings
from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess

from jobparser import settings
from jobparser.spiders.hhru import HhruSpider
from jobparser.spiders.sjru import SjruSpider

if __name__ == '__main__':
    # configure_logging()
    # settings_crawler = get_project_settings()
    # runner = CrawlerRunner(settings_crawler)
    #
    # runner.crawl(HhruSpider)
    # runner.crawl(SjruSpider)
    #
    # d = runner.join()
    # d.addBoth(lambda _: reactor.stop())
    #
    # reactor.run()

    settings_crawler = Settings()
    settings_crawler.setmodule(settings)

    crawler_process = CrawlerProcess(settings=settings_crawler)

    crawler_process.crawl(HhruSpider)
    # crawler_process.crawl(SjruSpider)

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


