from constants import REGISTER_ENDPOINT, LOGIN_ENDPOINT
from custom_requester.custom_requester import CustomRequester

class AuthAPI(CustomRequester):
    """
    Class for working with authentication
    """

    def __init__(self, session):
        super().__init__(session=session, base_url="https://auth.dev-cinescope.coconutqa.ru/")

    def register_user(self, user_data, expected_status=201):
        """
        Registration of the new user
        :param user_data: Data of the user
        :param expected_status: Expected status-code
        """
        return self.send_request(
            method = "POST",
            endpoint = REGISTER_ENDPOINT,
            data = user_data,
            expected_status = expected_status
        )

    def login_user(self, login_data, expected_status=201):
        """
        Authentication of the user
        :param login_data: Data for logging in (email, password)
        :param expected_status: Expected status-code
        """
        return self.send_request(
            method = "POST",
            endpoint = LOGIN_ENDPOINT,
            data = login_data,
            expected_status = expected_status
        )

    def authenticate(self, user_creds):
        login_data = {
            "email": user_creds[0],
            "password": user_creds[1]
        }

        response = self.login_user(login_data).json()
        if "accessToken" not in response:
            raise KeyError("accessToken is missing!")

        token = response["accessToken"]
        self._update_session_headers(**{"authorization": "Bearer " + token})