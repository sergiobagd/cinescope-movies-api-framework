from clients.api_manager import ApiManager
from constants.constants import MOVIES_ENDPOINT
import pytest


class TestMoviesAPI:
    def test_get_movies_list(self, api_manager: ApiManager):
        response = api_manager.movies_api.get_movies_list()
        response_data = response.json()

        assert response_data["movies"] is not None

    def test_get_movies_list_by_filters(self, api_manager: ApiManager):
        payload = {
            "locations": "MSK",
            "minPrice": 1,
            "maxPrice": 500,
            "pageSize": 10
        }
        response = api_manager.movies_api.get_movies_list(params=payload)
        response_data = response.json()

        assert response_data["movies"] is not None
        assert (len(response_data["movies"])) == 10
        for movie in response_data["movies"]:
            assert movie["location"] == 'MSK'
            assert 1 <= movie["price"] <= 500

    def test_create_movie(self, super_admin, test_movie):

        response = super_admin.api.movies_api.create_new_movie(test_movie)
        response_data = response.json()

        assert response_data["id"] is not None

    def test_get_specific_movie(self, super_admin, created_movie):
        response = super_admin.api.movies_api.get_specific_movie(created_movie["id"])
        response_data = response.json()

        assert created_movie["id"] == response_data["id"]
        assert created_movie["name"] == response_data["name"]

    def test_edit_movie(self, super_admin, created_movie):
        edited_movie_data = {
            "name": created_movie["name"] + ' EDITED'
        }
        response = super_admin.api.movies_api.edit_movie(edited_movie_data, created_movie["id"])
        response_data = response.json()

        assert response_data["name"] != created_movie["name"]
        assert response_data["name"] == created_movie["name"] + ' EDITED'

    def test_delete_movie(self, super_admin, created_movie_for_deletion_test):
        response = super_admin.api.movies_api.delete_movie(created_movie_for_deletion_test["id"])
        response_data = response.json()

        assert created_movie_for_deletion_test["id"] == response_data["id"]

        response_get_deleted_movie = super_admin.api.movies_api.get_specific_movie(response_data["id"], expected_status=404).json()
        assert "message" in response_get_deleted_movie
        assert response_get_deleted_movie["message"] == "Фильм не найден", "Movie was found"

    @pytest.mark.parametrize("priceValues,locations,genreId", [
        ([200, 800], "MSK", 9),
        ([1, 200], "SPB", 1),
        ([1000, 2000], "MSK", 5)
    ], ids=["Animations with price from 200 to 800 from MSK",
            "Dramas with price from 1 to 200 from SPB",
            "Triller with price from 1000 to 2000 from MSK"
            ])
    def test_get_movies_list_by_parametrized_filters(self, priceValues, locations, genreId, super_admin):
        minPrice = priceValues[0]
        maxPrice = priceValues[1]
        payload = {
            "minPrice": minPrice,
            "maxPrice": maxPrice,
            "locations": locations,
            "genreId": genreId
        }
        response = super_admin.api.movies_api.get_movies_list(params=payload).json()

        movies_list = response["movies"]

        assert movies_list is not None
        for movie in movies_list:
            assert minPrice <= movie["price"] <= maxPrice
            assert locations == movie["location"]
            assert genreId == movie["genreId"]

    def test_try_create_movie_already_existing(self, super_admin, test_movie):
        already_existing_movie = test_movie.copy()
        already_existing_movie["name"] = "We."
        response = super_admin.api.movies_api.create_new_movie(already_existing_movie, expected_status=409)
        response_data = response.json()

        assert "id" not in response_data
        assert "message" in response_data
        assert response_data["message"] == "Фильм с таким названием уже существует", "Already existing movie was created"

    def test_try_create_movie_with_non_existing_genre_id(self, super_admin, test_movie):
        non_existing_genre_id_movie = test_movie.copy()
        non_existing_genre_id_movie["genreId"] = 109340909400034901
        response = super_admin.api.movies_api.create_new_movie(non_existing_genre_id_movie, expected_status=400)
        response_data = response.json()

        assert "id" not in response_data
        assert "message" in response_data
        assert response_data["message"] == "Некорректные данные", "Non existing genreId was accepted"

    def test_try_create_movie_with_empty_name(self, super_admin, test_movie):
        movie_with_empty_name = test_movie.copy()
        movie_with_empty_name["name"] = ""
        response = super_admin.api.movies_api.create_new_movie(movie_with_empty_name, expected_status=400)
        response_data = response.json()

        assert "id" not in response_data
        assert "message" in response_data
        assert response_data["message"] == ["name should not be empty"], "Empty name was accepted"

    def test_try_create_movie_with_incorrect_name_type(self, super_admin, test_movie):
        movie_with_incorrect_name_type = test_movie.copy()
        movie_with_incorrect_name_type["name"] = 1500
        response = super_admin.api.movies_api.create_new_movie(movie_with_incorrect_name_type, expected_status=400)
        response_data = response.json()

        assert "id" not in response_data
        assert "message" in response_data
        assert response_data["message"] == ["Поле name должно быть строкой"], "Incorrect name was accepted"

    def test_try_create_movie_with_incorrect_price_type(self, super_admin, test_movie):
        movie_with_incorrect_price_type = test_movie.copy()
        movie_with_incorrect_price_type["price"] = "Heisenberg"
        response = super_admin.api.movies_api.create_new_movie(movie_with_incorrect_price_type, expected_status=400)
        response_data = response.json()

        assert "id" not in response_data
        assert "message" in response_data
        assert response_data["message"] == ["Поле price должно быть числом"], "Incorrect price was accepted"

    def test_try_create_movie_with_empty_location(self, super_admin, test_movie):
        movie_with_empty_location = test_movie.copy()
        movie_with_empty_location["location"] = ""
        response = super_admin.api.movies_api.create_new_movie(movie_with_empty_location, expected_status=400)
        response_data = response.json()

        assert "id" not in response_data
        assert "message" in response_data
        assert response_data["message"] == ["Поле location должно быть одним из: MSK, SPB"], "Empty location was accepted"


    def test_try_create_movie_with_incorrect_imageUrl(self, super_admin, test_movie):
        movie_with_with_incorrect_imageUrl = test_movie.copy()
        movie_with_with_incorrect_imageUrl["imageUrl"] = True
        response = super_admin.api.movies_api.create_new_movie(movie_with_with_incorrect_imageUrl, expected_status=400)
        response_data = response.json()

        assert "id" not in response_data
        assert "message" in response_data
        assert response_data["message"] == [
        "Неверная ссылка",
        "Поле imageUrl должно быть строкой"], "Incorrect imageUrl was accepted"

    def test_try_create_movie_with_incorrect_description(self, super_admin, test_movie):
        movie_with_with_incorrect_description = test_movie.copy()
        movie_with_with_incorrect_description["description"] = 2026
        response = super_admin.api.movies_api.create_new_movie(movie_with_with_incorrect_description, expected_status=400)
        response_data = response.json()

        assert "id" not in response_data
        assert "message" in response_data
        assert response_data["message"] == ["Поле description должно быть строкой"], "Wrong description was accepted"

    def test_try_create_movie_with_empty_published_status(self, super_admin, test_movie):
        movie_with_with_empty_published_status = test_movie.copy()
        movie_with_with_empty_published_status["published"] = None
        response = super_admin.api.movies_api.create_new_movie(movie_with_with_empty_published_status, expected_status=400)
        response_data = response.json()

        assert "id" not in response_data
        assert "message" in response_data
        assert response_data["message"] == ["Поле published должно быть булевым значением"], "Empty published status was accepted"

    def test_try_get_specific_non_existing_movie(self, api_manager: ApiManager):
        nonexisting_movie_id = 0
        response = api_manager.movies_api.get_specific_movie(nonexisting_movie_id, expected_status=404)
        response_data = response.json()

        assert nonexisting_movie_id not in response_data, "Non existing movie was found"
        assert "message" in response_data
        assert response_data["message"] == "Фильм не найден", "Movie was found"

    def test_try_get_movies_list_with_wrong_filters(self, api_manager: ApiManager):
        payload = {
            "location": "MSK",
            "minimumPrice": 125,
            "maximumPrice": 200,
            "pageLength": 20
        }
        response = api_manager.movies_api.get_movies_list(params=payload)
        response_data = response.json()

        assert response_data["movies"] is not None
        assert (len(response_data["movies"])) == 10, "Wrong 'pageLength' filter was accepted for request"
        for movie in response_data["movies"]:
            assert movie["location"] == 'MSK' or movie["location"] == 'SPB', "Wrong 'location' filter was accepted for request"
            assert 1 <= movie["price"] <= 1000000000, "Wrong 'minimumPrice' and 'maximumPrice' filters were accepted for request"

    @pytest.mark.slow
    def test_try_delete_non_existing_movie(self, super_admin, created_movie_for_deletion_test):
        nonexisting_movie_id = created_movie_for_deletion_test["id"] + 13
        response = super_admin.api.movies_api.delete_movie(nonexisting_movie_id, expected_status=404)
        response_data = response.json()

        assert "message" in response_data
        assert response_data["message"] == "Фильм не найден", "Movie was found"

    def test_try_edit_non_existing_movie(self, super_admin, created_movie):
        nonexisting_movie_id = created_movie["id"] + 13
        response = super_admin.api.movies_api.edit_movie(created_movie, nonexisting_movie_id, expected_status=404)
        response_data = response.json()

        assert "message" in response_data
        assert response_data["message"] == "Фильм не найден", "Movie was found"

    def test_try_edit_movie_with_wrong_parameter(self, super_admin, created_movie):
        edited_movie_data = {
            "title": created_movie["name"] + ' EDITED'
        }
        response = super_admin.api.movies_api.edit_movie(edited_movie_data, created_movie["id"], expected_status=404)
        response_data = response.json()

        assert "message" in response_data
        assert response_data["message"] == "Фильм не найден", "Movie was found"

    @pytest.mark.slow
    def test_try_create_movie_by_common_user(self, common_user, test_movie):
        response = common_user.api.movies_api.create_new_movie(test_movie, expected_status=403)
        response_data = response.json()

        assert "message" in response_data
        assert response_data["message"] == "Forbidden resource", "Movie was created"

    @pytest.mark.parametrize("user_role,expected_status", [
        ("super_admin", 200),
        ("common_admin", 403),
        ("common_user", 403),
    ], ids = ["SuperAdmin", "Admin", "User"])
    @pytest.mark.slow
    def test_delete_movie_by_different_roles(self, request, user_role, expected_status, created_movie_for_deletion_test):
        user = request.getfixturevalue(user_role)
        user.api.movies_api.delete_movie(created_movie_for_deletion_test["id"], expected_status=expected_status)








