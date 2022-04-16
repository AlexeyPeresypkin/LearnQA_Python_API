from datetime import datetime

import requests

from lib.assertions import Assertions
from lib.base_case import BaseCase


class TestUserRegister(BaseCase):

    def setup(self):
        base_part = 'learnqa'
        domain = '@example.com'
        random_part = datetime.now().strftime('%m%d%Y%H%M%S')
        self.email = f'{base_part}{random_part}{domain}'

    def test_create_user_successfully(self):
        url = 'https://playground.learnqa.ru/api/user/'
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.email
        }
        response = requests.post(url, data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.asser_json_has_key(response, 'id')

    def test_create_user_with_existing_email(self):
        url = 'https://playground.learnqa.ru/api/user/'
        email = 'vinkotov@example.com'
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

        response = requests.post(url, data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            'utf-8') == f"Users with email '{email}' already exists", f'Unexpected response content {response.content}'