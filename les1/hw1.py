"""
1) Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев
для конкретного пользователя, сохранить JSON-вывод в файле *.json.

2) Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.
"""
import requests
import json
from pprint import pprint
import vk

def lst_github(selfusername='EuGeN-PYTHON'):
    username = input('Введите имя пользователя или нажмите Enter: ')
    if username == '':
        username = selfusername

    url = f"https://api.github.com/users/{username}/repos"

    user_data = requests.get(url).json()

    with open(f'{username}-repos.json', 'w', encoding='utf-8') as file:
        json.dump(user_data, file)
    ls = []
    for repo in user_data:
        ls.append(repo['name'])
    print(ls)

def get_group_vk(id = '7980512'):

    # user_id = input('Введите id пользователя  или нажмите Enter: ')
    # if user_id == '':
    #     user_id = id

    # url = f"https://oauth.vk.com/authorize?client_id={user_id}&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends&response_type=token&v=5.52"

    access_token = '9793a1e8fd9f3da8e4ee022ace7bec4a3e50b9a0aa97d3d2677106b17b540d95cc30b126a10a20b599e09'

    user_id = "561808790"

    url = f'https://api.vk.com/method/groups.get?user_id={user_id}&v=5.131&access_token={access_token}'

    user_data = requests.get(url).json()

    with open(f'vk_ID-{user_id}-groups.json', 'w', encoding='utf-8') as file:
        json.dump(user_data, file)

if __name__ == '__main__':
    lst_github()
    get_group_vk()