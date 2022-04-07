# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, Compose, TakeFirst

def salary_to_int(value):
    value = value.replace(' ', '')
    try:
        value = int(value)
    except:
        return value
    return value

# def clear_spec():


def specifications_get(div_list):
    list_spec = []
    for div in div_list:
        spec_dict = {}
        key_spec_dict = div[div.index('term') + 6:div.index('</dt>')]
        # key_spec_dict = key_spec_dict.replace(' ','')
        val_spec_dict = div[div.index('definition') + 12:div.index('</dd>')]
        val_spec_dict = val_spec_dict.replace('  ','').replace('\n','')
        spec_dict[key_spec_dict] = val_spec_dict
        list_spec.append(spec_dict)
    return list_spec


class StroyparserItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    salary = scrapy.Field(input_processor=MapCompose(salary_to_int), output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    specifications = scrapy.Field(output_processor=Compose(specifications_get))
