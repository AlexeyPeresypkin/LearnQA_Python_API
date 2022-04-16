import pytest
import requests

from lib.assertions import Assertions
from lib.base_case import BaseCase


class TestUserGet(BaseCase):

    def test_get_user_details_not_auth(self):
        url = 'https://playground.learnqa.ru/api/user/2'
        response = requests.get(url)
        print(response.content)

    assert 1 == 1
