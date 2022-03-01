"""
1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
которая будет добавлять только новые вакансии/продукты в вашу базу.

2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы
(необходимо анализировать оба поля зарплаты)

"""
import datetime

from pycbrf import ExchangeRates
from pprint import pprint
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from les2.hw2 import get_hh

client = MongoClient("mongodb+srv://evgeny_varlamov92:27Fifa2010@cluster0.pnfwt.mongodb.net/vacancies?retryWrites=true&w=majority")

db = client['vacancies']
hh = db.hh

def load_data_to_mongodb(data):
    not_added_data = []
    duplicate_data = []
    for one in data:
        one['_id'] = f'{one["link"][22:30]}_{one["link_site"][8:10]}'
        try:
            hh.insert_one(one)
        except DuplicateKeyError:
            duplicate_data.append(one)
        except:
            not_added_data.append(one)

def get_vacancies(currency):
    # currency = int(input('Введите минимальную сумму RUB, для фильтрации вакансий: '))
    now = datetime.datetime.now()
    rates = ExchangeRates(now.date())
    currency_dollar = currency / rates['USD'].value
    currency_dollar = int(currency_dollar)
    currency_euro = currency / rates['EUR'].value
    currency_euro = int(currency_euro)
    result = f"{{'$or':[{{'salary_ticket': 'RUB', 'salary_from': {{'$gte': {currency}}}}}," \
             f" {{'salary_ticket': 'USD', 'salary_from': {{'$gte': {currency_dollar}}}}}," \
             f" {{'salary_ticket': 'EUR', 'salary_from': {{'$gte': {currency_euro}}}}}," \
             f" {{'salary_ticket': 'RUB', 'salary_to': {{'$lte': {currency}}}}}," \
             f" {{'salary_ticket': 'USD', 'salary_to': {{'$lte': {currency_dollar}}}}}," \
             f" {{'salary_ticket': 'EUR', 'salary_to': {{'$lte': {currency_euro}}}}}]}}"

    result = eval(result)
    result = hh.find(result)
    try:
        for vacancy in result:
            pprint(vacancy)
    except:
        print('Данные не найдены')



if __name__ == '__main__':
    list_vacancies, search_word = get_hh()
    load_data_to_mongodb(list_vacancies)
    currency = int(input('Введите минимальную сумму RUB, для фильтрации вакансий: '))
    get_vacancies(currency)