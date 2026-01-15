from custom_requester.custom_requester import CustomRequester
class UserAPI(CustomRequester):
    """
    Class for working with Users API
    """

    def __init__(self, session):
        super().__init__(session=session, base_url="https://auth.dev-cinescope.coconutqa.ru/")
        self.session = session

    def get_user_info(self, user_id, expected_status=200):
        """
        Getting information about the user
        :param user_id: ID of the user
        :param expected_status: Expected status-code
        """
        return self.send_request(
            method = "GET",
            endpoint = f"/users/{user_id}",
            expected_status = expected_status
        )

    def delete_user(self, user_id, expected_status=204):
        """
        Deleting a specific user via ID
        :param user_id: ID of the user
        :param expected_status: Expected status code
        """
        return self.send_request(
            method = "DELETE",
            endpoint = f"/users/{user_id}",
            expected_status = expected_status
        )
