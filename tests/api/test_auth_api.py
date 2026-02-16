import datetime
import pytest_check as check
import allure
from pytest_mock import mocker
from constants.models import TestUser
from clients.api_manager import ApiManager
from constants.roles import Roles
from constants.models import RegisterUserResponse, AuthenticatedUserResponse


class TestAuthAPI:
    def test_register_user(self, api_manager: ApiManager, test_user):
        """
        Test for user registration
        """
        # Send request for register a user
        response = api_manager.auth_api.register_user(test_user)
        response_data = response.json()
        registered_user_response = RegisterUserResponse(**response_data)

        assert test_user.email == registered_user_response.email, "Emails are not equal"

    @allure.title("Test of user registration using mocker")
    @allure.severity(allure.severity_level.MINOR)
    @allure.label("qa_name", "Ivan Petrovich")
    def test_register_user_mock(self, api_manager: ApiManager, test_user: TestUser, mocker):
        with allure.step("Fake response from mock service"):
            mock_response = RegisterUserResponse(
                id = "id",
                email = "email@email.com",
                fullName = "fullName",
                verified = True,
                banned = False,
                roles = [Roles.SUPER_ADMIN],
                createdAt = str(datetime.datetime.now())
            )

        with allure.step("Mock method register_user in auth_api"):
            mocker.patch.object(
                api_manager.auth_api, # Object we mock
                'register_user', # Method we mock
                return_value=mock_response # Fake response
            )

        with allure.step("Call method which need to be mocked"):
            register_user_response = api_manager.auth_api.register_user(test_user)

        with allure.step("Check that response matches expected mocked response"):
            with allure.step("Check personal data"):
                check.equal(register_user_response.email, mock_response.email)
                check.equal(register_user_response.fullName, "INCORRECT FULL NAME", "NAMES DON'T MATCHING")

            with allure.step("Check field 'banned'"):
                check.equal(register_user_response.banned, mock_response.banned)


    def test_register_and_authenticate_user(self, api_manager: ApiManager, registered_user):
        # Send request for register a user
        response = api_manager.auth_api.login_user(registered_user)
        response_data = response.json()

        authenticated_user_response = AuthenticatedUserResponse(**response_data)
        assert registered_user["email"] == authenticated_user_response.user.email, "Emails are not equal"

    def test_try_register_user_with_different_passwords(self, api_manager: ApiManager, test_user):
        user_with_different_passwords = test_user
        user_with_different_passwords.passwordRepeat = user_with_different_passwords.password + "12"

        response = api_manager.auth_api.register_user(user_with_different_passwords, expected_status=400).json()

        assert "message" in response
        assert response["message"] == ["Пароли не совпадают"]

    def test_try_register_user_with_too_long_password(self, api_manager: ApiManager, test_user):
        user_with_too_long_password = test_user
        user_with_too_long_password.password = test_user.password + "100000002002303200002020200210200202"
        user_with_too_long_password.passwordRepeat = user_with_too_long_password.password

        response = api_manager.auth_api.register_user(user_with_too_long_password, expected_status=400).json()
        assert "message" in response
        assert response["message"] == ["Максимальная длина пароля 32 символа"]

    def test_try_register_user_with_not_allowed_symbols_password(self, api_manager: ApiManager, test_user):
        user_with_not_allowed_symbols_password = test_user
        user_with_not_allowed_symbols_password.password = test_user.password + "այբուբեն"
        user_with_not_allowed_symbols_password.passwordRepeat = user_with_not_allowed_symbols_password.password

        response = api_manager.auth_api.register_user(user_with_not_allowed_symbols_password, expected_status=400).json()
        assert "message" in response
        assert response["message"] == ["Пароль может содержать только буквы, цифры, спецсимволы и знаки: ~!?@#$%^&*_-+()[{}><>/\\|\"'.,:]"]

    def test_try_authenticate_user_with_wrong_password(self, api_manager: ApiManager, registered_user):
        # Data for log in the test user
        login_data = {
            "email": registered_user["email"],
            "password": 'blabla1488'
        }
        # Send request for register a user
        response = api_manager.auth_api.login_user(login_data, expected_status=401)
        response_data = response.json()

        # Assertions
        assert "accessToken" not in response_data, "Access Token is accessible when password is wrong"

    def test_try_authenticate_user_with_empty_password(self, api_manager: ApiManager, registered_user):
        # Data for log in the test user
        login_data = {
            "email": registered_user["email"],
            "password": ''
        }

        # Send request for register a user
        response = api_manager.auth_api.login_user(login_data, expected_status=401)
        response_data = response.json()

        # Assertions
        assert "accessToken" not in response_data, "Access Token is accessible when password is empty"

    def test_try_authenticate_user_with_empty_email(self, api_manager: ApiManager, registered_user):
        # Data for log in the test user
        login_data = {
            "email": '',
            "password": registered_user["password"]
        }
        # Send request for register a user
        response = api_manager.auth_api.login_user(login_data, expected_status=401)
        response_data = response.json()

        # Assertions
        assert "accessToken" not in response_data, "Access Token is accessible when email is empty"

    def test_try_authenticate_user_with_non_existing_email(self, api_manager: ApiManager, registered_user):
        # Data for log in the test user
        login_data = {
            "email": registered_user['email'] + 'mmm',
            "password": registered_user["password"]
        }

        # Send request for register a user
        response = api_manager.auth_api.login_user(login_data, expected_status=401)
        response_data = response.json()

        # Assertions
        assert "accessToken" not in response_data, "Access Token is accessible when email is non existing"

    def test_try_authenticate_user_with_empty_request_body(self, api_manager: ApiManager):
        # Data for log in the test user
        login_data = {}

        # Send request for register a user
        response = api_manager.auth_api.login_user(login_data, expected_status=401)
        response_data = response.json()

        # Assertions
        assert "accessToken" not in response_data, "Access Token is accessible when request body is empty"



