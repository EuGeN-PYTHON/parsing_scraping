import scrapy
from scrapy.http import HtmlResponse
from stroyparser.items import StroyparserItem
from scrapy.loader import ItemLoader


class LmruSpider(scrapy.Spider):
    name = 'lmru'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://leroymerlin.ru/search/?q={kwargs.get("keyword")}']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-qa-pagination-item='right']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[@data-qa='product-image']")
        for link in links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=StroyparserItem(), response=response)
        loader.add_xpath('name', '//h1/text()')
        # name_value = response.css('h1::text').get()
        loader.add_value('url', response.url)
        # url_value = response.url
        loader.add_xpath('salary', "//span[@slot='price']//text()")
        # salary_value = response.xpath("//span[@slot='price']//text()").get()
        loader.add_xpath('photos', '//source[@media=" only screen and (min-width: 1024px)"]/@srcset')
        # photos_value = response.xpath('//source[@media=" only screen and (min-width: 1024px)"]/@srcset').getall()
        # specifications_div_list = response.xpath("//div[@class='def-list__group']").getall()
        # spec_dict = self.specifications_get(specifications_div_list)
        # loader.add_value('specifications', spec_dict)
        loader.add_xpath('specifications', "//div[@class='def-list__group']")
        yield loader.load_item()
        # yield StroyparserItem(name=name_value, url=url_value, salary=salary_value, photos=photos_value, specifications=specifications_value)

    # def specifications_get(self, div_list):
    #     list_specifications = []
    #     for div in div_list:
    #         spec_dict = {}
    #         key_spec_dict = div[div.index('term')+6:div.index('</dt>')]
    #         val_spec_dict = div[div.index('definition')+12:div.index('</dd>')]
    #         spec_dict[key_spec_dict] = val_spec_dict
    #         list_specifications.append(spec_dict)
    #     return list_specifications


