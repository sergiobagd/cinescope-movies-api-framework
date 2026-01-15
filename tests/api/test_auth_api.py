from clients.api_manager import ApiManager


class TestAuthAPI:
    def test_register_user(self, api_manager: ApiManager, test_user):
        """
        Test for user registration
        """
        # Send request for register a user
        response = api_manager.auth_api.register_user(test_user)
        response_data = response.json()

        assert test_user["email"] == response_data.get("email"), "Emails are not equal"
        assert "id" in response_data, "ID of the user is missing"
        assert "roles" in response_data, "Roles of the user are missing"
        # Assert that role "USER" is set by default
        assert "USER" in response_data["roles"], "Role 'USER' should be added to the new user"

    def test_register_and_authenticate_user(self, api_manager: ApiManager, registered_user):
        # Data for log in the test user
        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }

        # Send request for register a user
        response = api_manager.auth_api.login_user(login_data)
        response_data = response.json()

        assert login_data["email"] == response_data["user"]["email"], "Emails are not equal"
        assert "id" in response_data["user"], "ID of the user is missing"
        assert "accessToken" in response_data, "Access Token is missing"

    def test_try_register_user_with_different_passwords(self, api_manager: ApiManager, test_user_different_password):
        response = api_manager.auth_api.register_user(test_user_different_password, expected_status = 400)
        assert response.status_code == 400, "Registration was OK with different passwords"

    def test_try_register_user_with_too_long_password(self, api_manager: ApiManager, test_user_too_long_password):
        response = api_manager.auth_api.register_user(test_user_too_long_password, expected_status = 400)
        assert response.status_code == 400, "Registration was OK with too long password"

    def test_try_register_user_with_not_allowed_symbols_password(self, api_manager: ApiManager, test_user_not_allowed_symbols_password):
        response = api_manager.auth_api.register_user(test_user_not_allowed_symbols_password, expected_status = 400)
        assert response.status_code == 400, "Registration was OK with not allowed symbols in password"

    def test_try_authenticate_user_with_wrong_password(self, api_manager: ApiManager, registered_user):
        # Data for log in the test user
        login_data = {
            "email": registered_user["email"],
            "password": 'blabla1488'
        }
        # Send request for register a user
        response = api_manager.auth_api.login_user(login_data, expected_status = 401)
        response_data = response.json()

        # Assertions
        assert response.status_code == 401, "Authentication was OK with wrong password"
        assert "accessToken" not in response_data, "Access Token is accessible when password is wrong"

    def test_try_authenticate_user_with_empty_password(self, api_manager: ApiManager, registered_user):
        # Data for log in the test user
        login_data = {
            "email": registered_user["email"],
            "password": ''
        }

        # Send request for register a user
        response = api_manager.auth_api.login_user(login_data, expected_status = 401)
        response_data = response.json()

        # Assertions
        assert response.status_code == 401, "Authentication was OK with empty password"
        assert "accessToken" not in response_data, "Access Token is accessible when password is empty"

    def test_try_authenticate_user_with_empty_email(self, api_manager: ApiManager, registered_user):
        # Data for log in the test user
        login_data = {
            "email": '',
            "password": registered_user["password"]
        }
        # Send request for register a user
        response = api_manager.auth_api.login_user(login_data, expected_status = 401)
        response_data = response.json()

        # Assertions
        assert response.status_code == 401, "Authentication was OK with empty email"
        assert "accessToken" not in response_data, "Access Token is accessible when email is empty"

    def test_try_authenticate_user_with_non_existing_email(self, api_manager: ApiManager, registered_user):
        # Data for log in the test user
        login_data = {
            "email": registered_user['email'] + 'mmm',
            "password": registered_user["password"]
        }

        # Send request for register a user
        response = api_manager.auth_api.login_user(login_data, expected_status = 401)
        response_data = response.json()

        # Assertions
        assert response.status_code == 401, "Authentication was OK with non existing email"
        assert "accessToken" not in response_data, "Access Token is accessible when email is non existing"

    def test_try_authenticate_user_with_empty_request_body(self, api_manager: ApiManager):
        # Data for log in the test user
        login_data = {}

        # Send request for register a user
        response = api_manager.auth_api.login_user(login_data, expected_status = 401)
        response_data = response.json()

        # Assertions
        assert response.status_code == 401, "Authentication was OK with empty request body"
        assert "accessToken" not in response_data, "Access Token is accessible when request body is empty"



