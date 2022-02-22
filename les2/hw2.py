"""
Необходимо собрать информацию о вакансиях на вводимую должность
(используем input или через аргументы получаем должность) с сайтов HH(обязательно)
и/или Superjob(по желанию). Приложение должно анализировать несколько страниц сайта
(также вводим через input или аргументы). Получившийся список должен содержать в себе минимум:

Наименование вакансии.
Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
Ссылку на саму вакансию.
Сайт, откуда собрана вакансия.
"""

import requests
import json
from bs4 import BeautifulSoup

from pprint import pprint

# 'https://hh.ru/search/vacancy?area=1&fromSearchLine=true&text=Python&from=suggest_post&page=0&hhtmFrom=vacancy_search_list'
# https://hh.ru/search/vacancy?area=1&fromSearchLine=true&text=python


base_url = 'https://hh.ru'
search_word = input('Введите ключевое слово для поиска вакансии: ')
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
params = {'area': 1, 'fromSearchLine': 'true', 'text': {search_word}, 'page': 0, 'hhtmFrom': 'vacancy_search_list',
          'from': 'suggest_post', 'clusters':'true', 'ored_clusters': 'true'}
# #a11y-main-content > div:nth-child(1) > div.vacancy-serp-item-body > div.vacancy-serp-item-body__main-info
url = f'{base_url}/search/vacancy'

response = requests.get(url, headers=headers, params=params)
dom = BeautifulSoup(response.text, 'html.parser')

pager = dom.find('div', {'class': 'pager'})
pager_count = pager.find('a', {'data-qa': 'pager-next'}).previousSibling
count_page = pager_count.find('a', {'data-qa': 'pager-page'}).text
count_page = int(count_page)

list_vacancies = []

def dump_json(data, search_word):
    with open(f'{search_word}-vacancies.json', 'w', encoding='utf-8') as file:
        json.dump(data, file)

def get_hh():
    for i in range(count_page):
        response = requests.get(url, headers=headers, params=params)
        dom = BeautifulSoup(response.text, 'html.parser')
        vacancies = dom.find_all('div', {'class': 'vacancy-serp-item vacancy-serp-item_redesigned'})
        for vacancy in vacancies:
            one_vacancy = {}
            vac = vacancy.find('a', {'class': 'bloko-link'})
            name = vac.text
            link = vac['href']
            name_company = vacancy.find('a', {'class': 'bloko-link bloko-link_kind-tertiary'}).text
            link_site = base_url
            one_vacancy['name'] = name
            one_vacancy['link'] = link
            one_vacancy['name_company'] = name_company
            one_vacancy['link_site'] = link_site
            salary_list = []
            if vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}):
                salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).text
                salary = salary.split()
                if salary[0] == 'от':
                    salary_list.append(int(f'{salary[1]}{salary[2]}'))
                    salary_list.append(None)
                    if salary[3] == 'руб.':
                        salary_list.append('RUB')
                    else:
                        salary_list.append(salary[3])
                elif salary[0] == 'до':
                    salary_list.append(None)
                    salary_list.append(int(f'{salary[1]}{salary[2]}'))
                    if salary[3] == 'руб.':
                        salary_list.append('RUB')
                    else:
                        salary_list.append(salary[3])
                else:
                    salary_list.append(int(f'{salary[0]}{salary[1]}'))
                    salary_list.append(int(f'{salary[3]}{salary[4]}'))
                    if salary[5] == 'руб.':
                        salary_list.append('RUB')
                    else:
                        salary_list.append(salary[5])
                # one_vacancy['salary'] = salary_list
            else:
                salary_list.append(None)
                salary_list.append(None)
                salary_list.append(None)
            one_vacancy['salary'] = salary_list
            list_vacancies.append(one_vacancy)
        params['page'] += 1
    dump_json(list_vacancies, search_word)

if __name__ == '__main__':
    get_hh()
