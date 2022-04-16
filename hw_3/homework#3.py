import pytest
import requests

from mixins import user_agents, AsserJsonKey, BaseCaseForHW


class TestHomeWork(BaseCaseForHW):
    user_agents = user_agents

    def setup(self):
        self.url_1 = 'https://playground.learnqa.ru/api/homework_cookie'
        self.url_2 = 'https://playground.learnqa.ru/api/homework_header'
        self.url_3 = 'https://playground.learnqa.ru/ajax/api/user_agent_check'

    def test_cookie(self):
        resp = requests.get(self.url_1)
        cookie = self.get_cookie(resp, 'HomeWork', 'hw_value')

    def test_headers(self):
        resp = requests.get(self.url_2)
        header = self.get_headers(resp, 'x-secret-homework-header',
                                  'Some secret value')

    @pytest.mark.parametrize('user_agent, expected', user_agents)
    def test_user_agent(self, user_agent, expected):
        resp = requests.get(self.url_3, headers={'User-Agent': user_agent})
        values_result = AsserJsonKey.assert_json_value_contains(resp)
        platform_expected = expected['platform']
        browser_expected = expected['browser']
        device_expected = expected['device']
        assert platform_expected == values_result[
            'platform'], f'Response JSON with key platform not equal "{platform_expected}"'
        assert browser_expected == values_result[
            'browser'], f'Response JSON with key browser not equal "{browser_expected}"'
        assert device_expected == values_result[
            'device'], f'Response JSON with key device not equal "{device_expected}"'
