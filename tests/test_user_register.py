from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


class TestUserRegister(BaseCase):

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post('/user', data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.asser_json_has_key(response, 'id')

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email=email)

        response = MyRequests.post('/user', data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            'utf-8') == f"Users with email '{email}' already exists", f'Unexpected response content {response.content}'

    def test_create_user_with_incorrect_email(self):
        email = 'vinkotovexample.com'
        data = self.prepare_registration_data(email=email)

        response = MyRequests.post('/user', data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            'utf-8') == f"Invalid email format", f'Unexpected response content {response.content}'

    def test_create_user_without_field(self):
        data_without_email = self.prepare_registration_data_without_field(
            'email')
        data_without_password = self.prepare_registration_data_without_field(
            'password')
        data_without_username = self.prepare_registration_data_without_field(
            'username')
        data_without_firstname = self.prepare_registration_data_without_field(
            'firstName')
        data_without_lastname = self.prepare_registration_data_without_field(
            'lastName')

        response_wo_email = MyRequests.post('/user', data=data_without_email)
        response_wo_password = MyRequests.post('/user',
                                               data=data_without_password)
        response_wo_username = MyRequests.post('/user',
                                               data=data_without_username)
        response_wo_firstname = MyRequests.post('/user',
                                                data=data_without_firstname)
        response_wo_lastname = MyRequests.post('/user',
                                               data=data_without_lastname)

        Assertions.assert_code_status(response_wo_email, 400)
        assert response_wo_email.content.decode(
            'utf-8') == f"The following required params are missed: email", f'Unexpected response content {response_wo_email.content}'

        Assertions.assert_code_status(response_wo_password, 400)
        assert response_wo_password.content.decode(
            'utf-8') == f"The following required params are missed: password", f'Unexpected response content {response_wo_password.content}'

        Assertions.assert_code_status(response_wo_username, 400)
        assert response_wo_username.content.decode(
            'utf-8') == f"The following required params are missed: username", f'Unexpected response content {response_wo_username.content}'

        Assertions.assert_code_status(response_wo_firstname, 400)
        assert response_wo_firstname.content.decode(
            'utf-8') == f"The following required params are missed: firstName", f'Unexpected response content {response_wo_firstname.content}'

        Assertions.assert_code_status(response_wo_lastname, 400)
        assert response_wo_lastname.content.decode(
            'utf-8') == f"The following required params are missed: lastName", f'Unexpected response content {response_wo_lastname.content}'

    def test_create_user_with_long_or_short_username(self):
        data_with_short_name = self.prepare_registration_data()
        data_with_long_name = self.prepare_registration_data()
        data_with_short_name['username'] = 'a'
        data_with_long_name['username'] = 'a' * 251

        response_with_short_name = MyRequests.post(
            '/user',
            data=data_with_short_name
        )
        response_with_long_name = MyRequests.post(
            '/user',
            data=data_with_long_name
        )

        Assertions.assert_code_status(response_with_short_name, 400)
        assert response_with_short_name.content.decode(
            'utf-8') == f"The value of 'username' field is too short", f'Unexpected response content {response_with_short_name.content}'

        Assertions.assert_code_status(response_with_long_name, 400)
        assert response_with_long_name.content.decode(
            'utf-8') == f"The value of 'username' field is too long", f'Unexpected response content {response_with_long_name.content}'
