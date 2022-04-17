import pytest
import requests

from lib.assertions import Assertions
from lib.base_case import BaseCase


class TestUserGet(BaseCase):

    def test_get_user_details_not_auth(self):
        url = 'https://playground.learnqa.ru/api/user/2'
        response = requests.get(url)

        Assertions.asser_json_has_key(response, 'username')
        Assertions.asser_json_has_not_key(response, 'email')
        Assertions.asser_json_has_not_key(response, 'firstName')
        Assertions.asser_json_has_not_key(response, 'lastName')

    def test_get_user_details_auth_as_same_user(self):
        url = 'https://playground.learnqa.ru/api/user/login'
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response = requests.post(url, data=data)
        auth_sid = self.get_cookie(response, 'auth_sid')
        token = self.get_header(response, 'x-csrf-token')
        user_id_from_auth_method = self.get_json_value(response, 'user_id')

        response2 = requests.get(
            f'https://playground.learnqa.ru/api/user/{user_id_from_auth_method}',
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid}
        )

        Assertions.asser_json_has_keys(
            response2,
            ['username', 'email', 'firstName', 'lastName']
        )
