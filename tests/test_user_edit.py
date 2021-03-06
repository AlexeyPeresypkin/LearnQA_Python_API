from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserEdit(BaseCase):

    def setup(self):
        self.register_data_1 = self.prepare_registration_data()
        self.register_data_2 = self.prepare_registration_data()

    def test_edit_just_created_user(self):
        # REGISTER
        response1 = MyRequests.post('/user', data=self.register_data_1)

        Assertions.assert_code_status(response1, 200)
        Assertions.asser_json_has_key(response1, 'id')

        email = self.register_data_1['email']
        password = self.register_data_1['password']
        user_id = self.get_json_value(response1, 'id')

        # LOGIN
        logind_data = {
            'email': email,
            'password': password,
        }
        response2 = MyRequests.post('/user/login', data=logind_data)

        auth_sid = self.get_cookie(response2, 'auth_sid')
        token = self.get_header(response2, 'x-csrf-token')

        # EDIT USER
        new_name = 'ChangedName'
        response3 = MyRequests.put(
            f'/user/{user_id}',
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid},
            data={'firstName': new_name}
        )

        Assertions.assert_code_status(response3, 200)

        # CHECK CHANGED DATA
        response4 = MyRequests.get(
            f'/user/{user_id}',
            headers={'x-csrf-token': token},
            cookies={'auth_sid': auth_sid},
        )

        Assertions.assert_json_value_by_name(
            response4,
            'firstName',
            new_name,
            'Wrong name of the user after edit'
        )

    def test_edit_user_without_login(self):
        response1 = MyRequests.post('/user', data=self.register_data_1)
        user_id = self.get_json_value(response1, 'id')
        new_name = 'ChangedName'
        response2 = MyRequests.put(
            f'/user/{user_id}',
            data={'firstName': new_name}
        )
        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode('utf-8') == f'Auth token not supplied', f'Unexpected response content {response2.content}'
