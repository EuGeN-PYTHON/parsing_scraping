import re
import json
import scrapy
from scrapy.http import HtmlResponse
from instagramparser.items import InstagramparserItem
from urllib.parse import urlencode
from copy import deepcopy


class InstagramspiderSpider(scrapy.Spider):
    name = 'InstagramSpider'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']
    log_link = 'https://www.instagram.com/accounts/login/ajax/'
    passwd_inst = '#PWD_INSTAGRAM_BROWSER:10:1649238605:AeRQANe8s/WAKc9IlFBzEG7afkOOkv7VS1N2ofE9V52xJjZjrWrslcDnOcV9tHMEVk0bGVkQyfzrAYoxhX7znA4mc49XMxvMNfucEvjA8ippn0z80Ca7Ip71fzpK69YFKYnkiIl322Q5z+8SLyU='
    login_inst = 'Onliskill_udm'
    user_for_parse = 'techskills_2022'
    inst_graphql_link = 'https://www.instagram.com/graphql/query/?'
    posts_hash = '396983faee97f4b49ccbe105b4daf7a0'
    friendships_link = 'https://i.instagram.com/api/v1/friendships/'
    inst_headers = {'': ''}

    def parse(self, response: HtmlResponse):
        token = self.get_csrf(response.text)
        yield scrapy.FormRequest(
            self.log_link,
            method='POST',
            callback=self.login,
            formdata={'username': self.login_inst, 'enc_password': self.passwd_inst},
            headers={'X-CSRFToken': token}
        )

    def login(self, response: HtmlResponse):
        j_data = response.json()
        if j_data['authenticated']:
            yield response.follow(
                f'/{self.user_for_parse}',
                callback=self.user_data_parse,
                cb_kwargs={'username': self.user_for_parse}
            )

    def user_data_parse(self, response: HtmlResponse, username):
        user_id = self.get_userid(response.text, username)
        variables = {'count': 12,
                     'search_surface': 'follow_list_page'}
        type_user = 'followers'
        url_posts = f'{self.friendships_link}{user_id}/{type_user}/?{urlencode(variables)}'

        yield response.follow(
            url_posts,
            callback=self.user_posts_parse,
            headers={'User-Agent': 'Instagram 155.0.0.37.107'},
            cb_kwargs={'username': username,
                       'type_user': type_user,
                       'user_id': user_id,
                       'variables': deepcopy(variables)}

        )
        var = {'count': 12,
               'max_id': 12}
        type_user = 'following'
        url_posts = f'{self.friendships_link}{user_id}/{type_user}/?{urlencode(var)}'
        yield response.follow(
            url_posts,
            callback=self.user_posts_parse,
            headers={'User-Agent': 'Instagram 155.0.0.37.107'},
            cb_kwargs={'username': username,
                       'user_id': user_id,
                       'type_user': type_user,
                       'variables': deepcopy(var)}

        )

    def user_posts_parse(self, response: HtmlResponse, username, user_id, type_user, variables):
        j_data = response.json()
        if j_data.get('next_max_id'):
            variables['max_id'] = j_data.get('next_max_id')
            url_posts = f'{self.friendships_link}{user_id}/{type_user}/?{urlencode(variables)}'
            yield response.follow(url_posts,
                                  callback=self.user_posts_parse,
                                  headers={'User-Agent': 'Instagram 155.0.0.37.107'},
                                  cb_kwargs={'username': username, 'user_id': user_id,
                                             'type_user': type_user,
                                             'variables': deepcopy(variables)})

        users = j_data.get('users')
        for user in users:
            item = InstagramparserItem(
                user_id_main=user_id,
                username_main=username,
                type_user=type_user,
                user_photo=user.get('profile_pic_url'),
                user_id=user.get('pk'),
                user_name=user.get('username')
            )
            yield item


    def get_csrf(self, text):
        token = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return token.split(':').pop().replace(r'"', '')

    def get_userid(self, text, username):
        try:
            matched = re.search(
                '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
            ).group()
            return json.loads(matched).get('id')
        except:
            return re.findall('\"id\":\"\\d+\"', text)[-1].split('"')[-2]
