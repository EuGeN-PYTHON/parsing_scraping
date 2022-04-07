# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import re

class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy_scrapy
    def process_item(self, item, spider):
        print()
        if spider.name == "hhru":
            self.unzip_salary_hhru(item)
        else:
            self.unzip_salary_sjru(item)

        #Добавление в MongoDB
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

    def unzip_salary_hhru(self, item):
        if len(item['salary_list']) < 6 and 'от' in item['salary_list'][0]:
            salary_min = ''.join(item['salary_list'][1].split())
            item['salary_min'] = int(salary_min)
            item['salary_max'] = None
            item['salary_currency'] = item['salary_list'][3]
            item['salary_tax'] = item['salary_list'][4]
        elif len(item['salary_list']) < 6 and 'до' in item['salary_list'][0]:
            salary_max = ''.join(item['salary_list'][1].split())
            item['salary_min'] = None
            item['salary_max'] = int(salary_max)
            item['salary_currency'] = item['salary_list'][3]
            item['salary_tax'] = item['salary_list'][4]
        elif len(item['salary_list']) >= 6:
            salary_min = ''.join(item['salary_list'][1].split())
            salary_max = ''.join(item['salary_list'][3].split())
            item['salary_min'] = int(salary_min)
            item['salary_max'] = int(salary_max)
            item['salary_currency'] = item['salary_list'][5]
            item['salary_tax'] = item['salary_list'][6]
        else:
            item['salary_min'] = None
            item['salary_max'] = None
            item['salary_currency'] = None
            item['salary_tax'] = None
        return item

    def unzip_salary_sjru(self, item):
        if len(item['salary_list']) < 6 and 'от' in item['salary_list'][0]:
            salary_min = "".join(re.findall(r'\d+', item['salary_list'][2]))
            salary_currency = "".join(re.findall(r'\D+', item['salary_list'][2]))
            item['salary_min'] = int(salary_min)
            item['salary_max'] = None
            item['salary_currency'] = salary_currency
            item['salary_tax'] = None
        elif len(item['salary_list']) == 1:
            item['salary_min'] = None
            item['salary_max'] = None
            item['salary_currency'] = None
            item['salary_tax'] = None
        elif len(item['salary_list']) < 6 and 'до' in item['salary_list'][0]:
            salary_max = "".join(re.findall(r'\d+', item['salary_list'][2]))
            salary_currency = "".join(re.findall(r'\D+', item['salary_list'][2]))
            item['salary_min'] = None
            item['salary_max'] = int(salary_max)
            item['salary_currency'] = salary_currency
            item['salary_tax'] = None
        elif len(item['salary_list']) >= 6:
            salary_min = ''.join(item['salary_list'][0].split())
            salary_max = ''.join(item['salary_list'][4].split())
            item['salary_min'] = int(salary_min)
            item['salary_max'] = int(salary_max)
            item['salary_currency'] = item['salary_list'][6]
            item['salary_tax'] = None
        else:
            item['salary_min'] = None
            item['salary_max'] = None
            item['salary_currency'] = None
            item['salary_tax'] = None
        return item




