from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


class TestUserGet(BaseCase):

    def test_get_user_details_not_auth(self):
        response = MyRequests.get('/user/2')

        Assertions.asser_json_has_key(response, 'username')
        Assertions.asser_json_has_not_key(response, 'email')
        Assertions.asser_json_has_not_key(response, 'firstName')
        Assertions.asser_json_has_not_key(response, 'lastName')

    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response = MyRequests.post('/user/login', data=data)
        auth_sid = self.get_cookie(response, 'auth_sid')
        token = self.get_header(response, 'x-csrf-token')
        user_id_from_auth_method = self.get_json_value(response, 'user_id')

        response2 = MyRequests.get(
            f'/user/{user_id_from_auth_method}',
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid}
        )

        Assertions.asser_json_has_keys(
            response2,
            ['username', 'email', 'firstName', 'lastName']
        )

    def test_get_user_details_auth_as_other_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response = MyRequests.post('/user/login', data=data)
        auth_sid = self.get_cookie(response, 'auth_sid')
        token = self.get_header(response, 'x-csrf-token')

        response2 = MyRequests.get(
            f'/user/1',
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid}
        )
        Assertions.asser_json_has_key(response2, 'username')
        Assertions.asser_json_has_not_key(response2, 'email')
        Assertions.asser_json_has_not_key(response2, 'firstName')
        Assertions.asser_json_has_not_key(response2, 'lastName')
