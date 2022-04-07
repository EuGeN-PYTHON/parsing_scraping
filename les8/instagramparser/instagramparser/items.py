# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstagramparserItem(scrapy.Item):
    user_id_main = scrapy.Field()
    username_main = scrapy.Field()
    type_user = scrapy.Field()
    user_photo = scrapy.Field()
    user_id = scrapy.Field()
    user_name = scrapy.Field()
