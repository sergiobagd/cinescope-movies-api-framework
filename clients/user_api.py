from custom_requester.custom_requester import CustomRequester


class UserAPI(CustomRequester):
    """
    Class for working with Users API
    """
    def __init__(self, session):
        self.session = session
        super().__init__(session=session, base_url="https://auth.dev-cinescope.coconutqa.ru/")

    def get_user_info(self, user_locator, expected_status=200):
        """
        Getting information about the user
        :param user_id: ID of the user
        :param expected_status: Expected status-code
        """
        return self.send_request(
            method="GET",
            endpoint=f"/user/{user_locator}",
            expected_status=expected_status
        )

    def create_user(self, user_data, expected_status=201):
        return self.send_request(
            method="POST",
            endpoint="/user",
            data=user_data,
            expected_status=expected_status
        )

    def update_user(self, user_data, user_id, expected_status=200):
        return self.send_request(
            method="PATCH",
            endpoint=f"/user/{user_id}",
            data=user_data,
            expected_status=expected_status
        )

    def delete_user(self, user_id, expected_status=204):
        """
        Deleting a specific user via ID
        :param user_id: ID of the user
        :param expected_status: Expected status code
        """
        return self.send_request(
            method="DELETE",
            endpoint=f"/users/{user_id}",
            expected_status=expected_status
        )
