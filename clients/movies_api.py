from constants import LOGIN_ENDPOINT, MOVIES_ENDPOINT
from custom_requester.custom_requester import CustomRequester

class MoviesAPI(CustomRequester):
    """
    Class for working with Movies API
    """

    def __init__(self, session):
        super().__init__(session=session, base_url="https://api.dev-cinescope.coconutqa.ru/")

    def get_movies_list(self, expected_status = 200):
        """
        Getting the list of the movies
        """
        return self.send_request(
            method = "GET",
            endpoint = MOVIES_ENDPOINT,
            expected_status = expected_status
        )

    def get_movies_list_by_filters(self, expected_status = 200):
        """
        Getting the list of the movies
        """
        return self.send_request(
            method = "GET",
            endpoint = f"{MOVIES_ENDPOINT}?locations=MSK&minPrice=1&maxPrice=500&pageSize=10",
            expected_status = expected_status
        )

    def get_movies_list_by_wrong_filters(self, expected_status = 200):
        """
        Getting the list of the movies
        """
        return self.send_request(
            method = "GET",
            endpoint = f"{MOVIES_ENDPOINT}?location=MSK&minimumPrice=125&maximumPrice=200&pageLength=20",
            expected_status = expected_status
        )


    def create_new_movie(self, movie_data, expected_status = 201):
        """
        Creating a new test movie
        """
        return self.send_request(
            method = "POST",
            endpoint = MOVIES_ENDPOINT,
            data = movie_data,
            expected_status = expected_status
        )

    def edit_movie(self, movie_data, movie_id, expected_status = 200):
        """
        Editing a movie
        """
        edited_movie_data = {
            "name": movie_data["name"] + ' EDITED'
        }
        return self.send_request(
            method = "PATCH",
            endpoint = f"{MOVIES_ENDPOINT}/{movie_id}",
            data = edited_movie_data,
            expected_status = expected_status
        )

    def edit_movie_with_wrong_parameter(self, movie_data, movie_id, expected_status = 404):
        """
        Editing a movie
        """
        edited_movie_data = {
            "title": movie_data["name"] + ' EDITED'
        }
        return self.send_request(
            method = "PATCH",
            endpoint = f"{MOVIES_ENDPOINT}/{movie_id}",
            data = edited_movie_data,
            expected_status = expected_status
        )

    def get_specific_movie(self, movie_id, expected_status = 200):
        """
        Getting info of specific movie
        """
        return self.send_request(
            method = "GET",
            endpoint = f"{MOVIES_ENDPOINT}/{movie_id}",
            expected_status = expected_status
        )

    def delete_movie(self, movie_id, expected_status = 200):
        """
        Deleting specific movie
        """
        return self.send_request(
            method = "DELETE",
            endpoint = f"{MOVIES_ENDPOINT}/{movie_id}",
            expected_status = expected_status
        )

    # def create_feedback_for_movie(self, movie_id, expected_status = 201):
    #     """
    #     Creating a feedback about the movie
    #     """

