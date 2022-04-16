import json

from requests import Response


class BaseCaseForHW:
    def get_cookie(self, response: Response, cookie_name, cookie_value):
        assert cookie_name in response.cookies, f'Cannot find cookie with name {cookie_name} in the last response'
        assert cookie_value in response.cookies[
            'HomeWork'], f'Cannot find cookie value with value {cookie_value} in the last response'
        return dict(response.cookies)

    def get_headers(self, response: Response, header_name, header_value):
        assert header_name in response.headers, f'Cannot find header with name {header_name} in the last response'
        assert header_value in response.headers[
            'x-secret-homework-header'], f'Cannot find header value with value {header_value} in the last response'
        return response.headers.get(header_name)


class AsserJsonKey:
    @staticmethod
    def assert_json_value_contains(response: Response):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f'Response is not in JSON format. Response text is {response.text}'

        assert 'platform' in response_as_dict, f'Response JSON does not have key "platform"'
        assert 'browser' in response_as_dict, f'Response JSON does not have key "browser"'
        assert 'device' in response_as_dict, f'Response JSON does not have key "device"'
        return {
            'platform': response_as_dict['platform'],
            'browser': response_as_dict['browser'],
            'device': response_as_dict['device']
        }


user_agents = [
    (
        'Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
        {'platform': 'Mobile', 'browser': 'No', 'device': 'Android'}
    ),
    (
        'Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1',
        {'platform': 'Mobile', 'browser': 'Chrome', 'device': 'iOS'}
    ),
    (
        'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
        {'platform': 'Googlebot', 'browser': 'Unknown',
         'device': 'Unknown'}
    ),
    (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0',
        {'platform': 'Web', 'browser': 'Chrome', 'device': 'No'}
    ),
    (
        'Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
        {'platform': 'Mobile', 'browser': 'No', 'device': 'iPhone'}
    ),
]
