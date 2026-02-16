from clients.api_manager import ApiManager
from constants.constants import MOVIES_ENDPOINT
import pytest
import allure

from utils.data_generator import DataGenerator


@allure.epic("Testing movies endpoints")
class TestMoviesAPI:
    @allure.feature("Testing of getting list of the movies")
    @allure.story("Validity of getting DEFAULT list of movies")
    @allure.description("""
                        This test checks validity of getting the list of movies.
                        Steps:
                        1. Send get_movies_list endpoint
                        2. Check it's not empty""")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Sergio Bagd")
    @allure.label("test_mood", "Positive")
    @allure.title("Test of getting movies list")
    @pytest.mark.api
    @pytest.mark.positive
    def test_get_movies_list(self, api_manager: ApiManager):
        with allure.step("Send get_movies_list request and check status-code"):
            response = api_manager.movies_api.get_movies_list()
            response_data = response.json()

        with allure.step("Check that list of movies is not empty"):
            assert response_data["movies"] is not None

    @allure.feature("Testing of getting list of the movies")
    @allure.story("Validity of getting CUSTOM filtered list of movies")
    @allure.description("""
                        This test checks validity of getting the filtered list of movies.
                        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Sergio Bagd")
    @allure.label("test_mood", "Positive")
    @allure.title("Test of getting filtered movies list")
    @pytest.mark.api
    @pytest.mark.positive
    def test_get_movies_list_by_filters(self, api_manager: ApiManager):
        payload = {
            "locations": "MSK",
            "minPrice": 1,
            "maxPrice": 500,
            "pageSize": 10
        }

        with allure.step(f"Send get_movies_list request with query params {payload}"):
            response = api_manager.movies_api.get_movies_list(params=payload)
            response_data = response.json()

        with allure.step("Check that movies list is not empty"):
            assert response_data["movies"] is not None

        with allure.step("Check that pageSize is 10"):
            assert (len(response_data["movies"])) == 10

        with allure.step("Check that every movie in the list is from MSK and price is between 1 and 500 rubles"):
            for movie in response_data["movies"]:
                assert movie["location"] == 'MSK'
                assert 1 <= movie["price"] <= 500

    @allure.feature("Testing of creating movie")
    @allure.story("Validity of creating movie")
    @allure.description("""
                        This test checks validity of creating the movie.
                        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Sergio Bagd")
    @allure.label("test_mood", "Positive")
    @allure.title("Test of creating movie")
    @pytest.mark.db
    @pytest.mark.api
    @pytest.mark.positive
    def test_create_movie(self, super_admin, db_helper, test_movie):
        with allure.step("Check if there is movie with same name in DB"):
            if db_helper.get_movie_by_name(test_movie["name"]) is not None:
                with allure.step("Change test_movie name to get rid of same names"):
                    test_movie["name"] = test_movie["name"] + DataGenerator.generate_random_movie_name()

        with allure.step("Create movie"):
            response = super_admin.api.movies_api.create_new_movie(test_movie)
            response_data = response.json()

        with allure.step(""" Check: 1. Movie id is not empty"""):
            assert response_data["id"] is not None

        with allure.step("Check movie in DB by ID"):
            assert db_helper.get_movie_by_id(response_data["id"]) is not None
            movie = db_helper.get_movie_by_id(response_data["id"])

        with allure.step(""" Check: 1. Movie name is expected"""):
            assert movie.name ==  test_movie["name"]
        with allure.step(""" Check: 1. Movie price is expected"""):
            assert movie.price == test_movie["price"]

        with allure.step("Clean up test movies"):
            response_deletion = super_admin.api.movies_api.delete_movie(response_data["id"]).json()

        with allure.step("Check that test movie is deleted in DB"):
            assert db_helper.get_movie_by_id(response_deletion["id"]) is None

    @allure.feature("Testing of getting movie by ID")
    @allure.story("Validity of getting exact movie by ID")
    @allure.description("""
                        This test checks validity of exact movie by ID.
                        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Sergio Bagd")
    @allure.label("test_mood", "Positive")
    @allure.title("Test of getting exact movie by ID")
    @pytest.mark.api
    @pytest.mark.positive
    def test_get_specific_movie(self, super_admin, created_movie):
        with allure.step("Send request of getting movie using ID of created movie in fixture"):
            response = super_admin.api.movies_api.get_specific_movie(created_movie["id"])
            response_data = response.json()

        with allure.step("Check id of movie is matching (we got the movie we created)"):
            assert created_movie["id"] == response_data["id"]

        with allure.step("Check name of movie is matching (we got the movie we created)"):
            assert created_movie["name"] == response_data["name"]

    @allure.feature("Testing of editing movie")
    @allure.story("Validity of editing movie")
    @allure.description("""
                        This test checks validity of editing movie name.
                        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Sergio Bagd")
    @allure.label("test_mood", "Positive")
    @allure.title("Test of editing movie name")
    @pytest.mark.db
    @pytest.mark.api
    @pytest.mark.positive
    def test_edit_movie(self, super_admin, created_movie, db_helper):
        edited_movie_data = {
            "name": created_movie["name"] + ' EDITED'
        }

        with allure.step("Send edit movie request with new movie name"):
            response = super_admin.api.movies_api.edit_movie(edited_movie_data, created_movie["id"])
            response_data = response.json()

        with allure.step("Check that movie name isn't equal previous name when it was just created"):
            assert response_data["name"] != created_movie["name"]

        with allure.step("Check that movie name was edited in DB also"):
            assert db_helper.get_movie_by_name(edited_movie_data["name"]).name == edited_movie_data["name"]

        with allure.step("Check that movie name was edited in the correct movie in DB by id"):
            assert db_helper.get_movie_by_id(created_movie["id"]).id == response_data["id"]

        with allure.step("Check that edited movie name is expected"):
            assert response_data["name"] == created_movie["name"] + ' EDITED'

    @allure.feature("Testing of deleting movie")
    @allure.story("Validity of deleting movie")
    @allure.description("""
                        This test checks validity of deleting movie.
                        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Sergio Bagd")
    @allure.label("test_mood", "Positive")
    @allure.title("Test of deleting movie")
    @pytest.mark.db
    @pytest.mark.api
    @pytest.mark.positive
    def test_delete_movie(self, super_admin, created_movie_for_deletion_test, db_helper):
        with allure.step("Send delete movie request using ID of created movie from fixture"):
            response = super_admin.api.movies_api.delete_movie(created_movie_for_deletion_test["id"])
            response_data = response.json()

        with allure.step("Check that ID od deleted movie in response was the same ID of created movie response"):
            assert created_movie_for_deletion_test["id"] == response_data["id"]

        with allure.step("Check that deleted movie doesn't exist by created movie ID via API"):
            response_get_deleted_movie = super_admin.api.movies_api.get_specific_movie(response_data["id"], expected_status=404).json()

        with allure.step("Check that error message exists and it's expected that movie was not found"):
            assert "message" in response_get_deleted_movie
            assert response_get_deleted_movie["message"] == "Фильм не найден", "Movie was found"

        with allure.step("Check that deleted movie doesn't exist in DB"):
            assert db_helper.get_movie_by_id(response_data["id"]) is None

    @allure.feature("Testing of getting list of the movies")
    @allure.story("Validity of getting CUSTOM filtered list of movies")
    @allure.description("""
                        This test checks validity of getting filtered movies list using parametrized test.
                        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Sergio Bagd")
    @allure.label("test_mood", "Positive")
    @allure.title("Test of getting movies by parametrized filters")
    @pytest.mark.api
    @pytest.mark.positive
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

        with allure.step("Send get_movies_list request with query parameters"):
            response = super_admin.api.movies_api.get_movies_list(params=payload).json()

        movies_list = response["movies"]

        with allure.step("Check that movies list in response isn't empty"):
            assert movies_list is not None

        with allure.step("Check that each movie price is in expected range, location is expected, genreId is expected"):
            for movie in movies_list:
                assert minPrice <= movie["price"] <= maxPrice
                assert locations == movie["location"]
                assert genreId == movie["genreId"]

    @allure.feature("Testing of creating movie")
    @allure.story("Validity of system behaviour when trying to create movie with bad data")
    @allure.description("""
                        This test checks validity of system behaviour when trying to create already existing movie.
                        """)
    @allure.severity(allure.severity_level.MINOR)
    @allure.label("qa_name", "Sergio Bagd")
    @allure.label("test_mood", "Negative")
    @allure.title("Test of trying to create already existing movie with existing name")
    @pytest.mark.api
    @pytest.mark.negative
    def test_try_create_movie_already_existing(self, super_admin, test_movie):
        already_existing_movie = test_movie.copy()
        already_existing_movie["name"] = "We."

        with allure.step("Try to create movie with existing name and make sure status-code == 409"):
            response = super_admin.api.movies_api.create_new_movie(already_existing_movie, expected_status=409)
            response_data = response.json()

        with allure.step("Check there is no ID in response"):
            assert "id" not in response_data

        with allure.step("Check there is a valid error message"):
            assert "message" in response_data
            assert response_data["message"] == "Фильм с таким названием уже существует", "Already existing movie was created"

    @allure.feature("Testing of creating movie")
    @allure.story("Validity of system behaviour when trying to create movie with bad data")
    @allure.description("""
                        This test checks validity of system behaviour when trying to create movie with non-existing genreId.
                        """)
    @allure.severity(allure.severity_level.MINOR)
    @allure.label("qa_name", "Sergio Bagd")
    @allure.label("test_mood", "Negative")
    @allure.title("Test of trying to create movie with non-existing genreId")
    @pytest.mark.api
    @pytest.mark.negative
    def test_try_create_movie_with_non_existing_genre_id(self, super_admin, test_movie):
        non_existing_genre_id_movie = test_movie.copy()
        non_existing_genre_id_movie["genreId"] = 109340909400034901

        with allure.step("Try to create movie with non-existing genreId and make sure status-code == 400"):
            response = super_admin.api.movies_api.create_new_movie(non_existing_genre_id_movie, expected_status=400)
            response_data = response.json()

        with allure.step("Check there is no ID in response"):
            assert "id" not in response_data

        with allure.step("Check there is a valid error message"):
            assert "message" in response_data
            assert response_data["message"] == "Некорректные данные", "Non existing genreId was accepted"

    @allure.feature("Testing of creating movie")
    @allure.story("Validity of system behaviour when trying to create movie with bad data")
    @allure.description("""
                        This test checks validity of system behaviour when trying to create movie with empty name.
                        """)
    @allure.severity(allure.severity_level.MINOR)
    @allure.label("qa_name", "Sergio Bagd")
    @allure.label("test_mood", "Negative")
    @allure.title("Test of trying to create movie with empty name")
    @pytest.mark.api
    @pytest.mark.negative
    def test_try_create_movie_with_empty_name(self, super_admin, test_movie):
        movie_with_empty_name = test_movie.copy()
        movie_with_empty_name["name"] = ""

        with allure.step("Try to create movie with empty name and make sure status-code == 400"):
            response = super_admin.api.movies_api.create_new_movie(movie_with_empty_name, expected_status=400)
            response_data = response.json()

        with allure.step("Check there is no ID in response"):
            assert "id" not in response_data

        with allure.step("Check there is a valid error message"):
            assert "message" in response_data
            assert response_data["message"] == ["name should not be empty"], "Empty name was accepted"

    @allure.feature("Testing of creating movie")
    @allure.story("Validity of system behaviour when trying to create movie with bad data")
    @allure.description("""
                        This test checks validity of system behaviour when trying to create movie with incorrect name type.
                        """)
    @allure.severity(allure.severity_level.MINOR)
    @allure.label("qa_name", "Sergio Bagd")
    @allure.label("test_mood", "Negative")
    @allure.title("Test of trying to create movie with incorrect name type")
    @pytest.mark.api
    @pytest.mark.negative
    def test_try_create_movie_with_incorrect_name_type(self, super_admin, test_movie):
        movie_with_incorrect_name_type = test_movie.copy()
        movie_with_incorrect_name_type["name"] = 1500

        with allure.step("Try to create movie with incorrect name type and make sure status-code == 400"):
            response = super_admin.api.movies_api.create_new_movie(movie_with_incorrect_name_type, expected_status=400)
            response_data = response.json()

        with allure.step("Check there is no ID in response"):
            assert "id" not in response_data

        with allure.step("Check there is a valid error message"):
            assert "message" in response_data
            assert response_data["message"] == ["Поле name должно быть строкой"], "Incorrect name was accepted"

    @allure.feature("Testing of creating movie")
    @allure.story("Validity of system behaviour when trying to create movie with bad data")
    @allure.description("""
                        This test checks validity of system behaviour when trying to create movie with incorrect price type.
                        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Sergio Bagd")
    @allure.label("test_mood", "Negative")
    @allure.title("Test of trying to create movie with incorrect price type")
    @pytest.mark.api
    @pytest.mark.negative
    def test_try_create_movie_with_incorrect_price_type(self, super_admin, test_movie):
        movie_with_incorrect_price_type = test_movie.copy()
        movie_with_incorrect_price_type["price"] = "Heisenberg"

        with allure.step("Try to create movie with incorrect price type and make sure status-code == 400"):
            response = super_admin.api.movies_api.create_new_movie(movie_with_incorrect_price_type, expected_status=400)
            response_data = response.json()

        with allure.step("Check there is no ID in response"):
            assert "id" not in response_data

        with allure.step("Check there is a valid error message"):
            assert "message" in response_data
            assert response_data["message"] == ["Поле price должно быть числом"], "Incorrect price was accepted"

    @allure.feature("Testing of creating movie")
    @allure.story("Validity of system behaviour when trying to create movie with bad data")
    @allure.description("""
                        This test checks validity of system behaviour when trying to create movie with empty location.
                        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Sergio Bagd")
    @allure.label("test_mood", "Negative")
    @allure.title("Test of trying to create movie with empty location")
    @pytest.mark.api
    @pytest.mark.negative
    def test_try_create_movie_with_empty_location(self, super_admin, test_movie):
        movie_with_empty_location = test_movie.copy()
        movie_with_empty_location["location"] = ""

        with allure.step("Try to create movie with empty location and make sure status-code == 400"):
            response = super_admin.api.movies_api.create_new_movie(movie_with_empty_location, expected_status=400)
            response_data = response.json()

        with allure.step("Check there is no ID in response"):
            assert "id" not in response_data

        with allure.step("Check there is a valid error message"):
            assert "message" in response_data
            assert response_data["message"] == ["Поле location должно быть одним из: MSK, SPB"], "Empty location was accepted"

    @allure.feature("Testing of creating movie")
    @allure.story("Validity of system behaviour when trying to create movie with bad data")
    @allure.description("""
                        This test checks validity of system behaviour when trying to create movie with incorrect imageUrl.
                        """)
    @allure.severity(allure.severity_level.MINOR)
    @allure.label("qa_name", "Sergio Bagd")
    @allure.label("test_mood", "Negative")
    @allure.title("Test of trying to create movie with incorrect imageUrl")
    @pytest.mark.api
    @pytest.mark.negative
    def test_try_create_movie_with_incorrect_imageUrl(self, super_admin, test_movie):
        movie_with_with_incorrect_imageUrl = test_movie.copy()
        movie_with_with_incorrect_imageUrl["imageUrl"] = True

        with allure.step("Try to create movie with incorrect imageUrl and make sure status-code == 400"):
            response = super_admin.api.movies_api.create_new_movie(movie_with_with_incorrect_imageUrl, expected_status=400)
            response_data = response.json()

        with allure.step("Check there is no ID in response"):
            assert "id" not in response_data

        with allure.step("Check there is a valid error message"):
            assert "message" in response_data
            assert response_data["message"] == [
            "Неверная ссылка",
            "Поле imageUrl должно быть строкой"], "Incorrect imageUrl was accepted"

    @allure.feature("Testing of creating movie")
    @allure.story("Validity of system behaviour when trying to create movie with bad data")
    @allure.description("""
                        This test checks validity of system behaviour when trying to create movie with incorrect description.
                        """)
    @allure.severity(allure.severity_level.MINOR)
    @allure.label("qa_name", "Sergio Bagd")
    @allure.label("test_mood", "Negative")
    @allure.title("Test of trying to create movie with incorrect description")
    @pytest.mark.api
    @pytest.mark.negative
    def test_try_create_movie_with_incorrect_description(self, super_admin, test_movie):
        movie_with_with_incorrect_description = test_movie.copy()
        movie_with_with_incorrect_description["description"] = 2026

        with allure.step("Try to create movie with incorrect description and make sure status-code == 400"):
            response = super_admin.api.movies_api.create_new_movie(movie_with_with_incorrect_description, expected_status=400)
            response_data = response.json()

        with allure.step("Check there is no ID in response"):
            assert "id" not in response_data

        with allure.step("Check there is a valid error message"):
            assert "message" in response_data
            assert response_data["message"] == ["Поле description должно быть строкой"], "Wrong description was accepted"

    @allure.feature("Testing of creating movie")
    @allure.story("Validity of system behaviour when trying to create movie with bad data")
    @allure.description("""
                        This test checks validity of system behaviour when trying to create movie with empty published status.
                        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Sergio Bagd")
    @allure.label("test_mood", "Negative")
    @allure.title("Test of trying to create movie with empty published status")
    @pytest.mark.api
    @pytest.mark.negative
    def test_try_create_movie_with_empty_published_status(self, super_admin, test_movie):
        movie_with_with_empty_published_status = test_movie.copy()
        movie_with_with_empty_published_status["published"] = None

        with allure.step("Try to create movie with empty published status and make sure status-code == 400"):
            response = super_admin.api.movies_api.create_new_movie(movie_with_with_empty_published_status, expected_status=400)
            response_data = response.json()

        with allure.step("Check there is no ID in response"):
            assert "id" not in response_data

        with allure.step("Check there is a valid error message"):
            assert "message" in response_data
            assert response_data["message"] == ["Поле published должно быть булевым значением"], "Empty published status was accepted"

    @allure.feature("Testing of getting movie by ID")
    @allure.story("Validity of system behaviour when trying to get movie with non-existing ID")
    @allure.description("""
                        This test checks validity of system behaviour when trying to get movie with non-existing ID.
                        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Sergio Bagd")
    @allure.label("test_mood", "Negative")
    @allure.title("Test of trying to get specific movie with non-existing ID")
    @pytest.mark.api
    @pytest.mark.negative
    def test_try_get_specific_non_existing_movie(self, api_manager: ApiManager):
        nonexisting_movie_id = 0

        with allure.step("Try to get movie with non-existing ID and make sure status-code == 404"):
            response = api_manager.movies_api.get_specific_movie(nonexisting_movie_id, expected_status=404)
            response_data = response.json()

        with allure.step("Check there is no non-existing ID in response"):
            assert nonexisting_movie_id not in response_data, "Non existing movie was found"

        with allure.step("Check there is a valid error message"):
            assert "message" in response_data
            assert response_data["message"] == "Фильм не найден", "Movie was found"

    @allure.feature("Testing of getting list of the movies")
    @allure.story("Validity of system behaviour when trying to get movies list with incorrect filters")
    @allure.description("""
                        This test checks validity of system behaviour when trying to get movies list with incorrect filters.
                        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Sergio Bagd")
    @allure.label("test_mood", "Negative")
    @allure.title("Test of trying to get movies list with incorrect filters")
    @pytest.mark.api
    @pytest.mark.negative
    def test_try_get_movies_list_with_wrong_filters(self, api_manager: ApiManager):
        payload = {
            "location": "MSK",
            "minimumPrice": 125,
            "maximumPrice": 200,
            "pageLength": 20
        }

        with allure.step("Get movies list"):
            response = api_manager.movies_api.get_movies_list(params=payload)
            response_data = response.json()

        with allure.step("Check movies list isn't empty"):
            assert response_data["movies"] is not None

        with allure.step("Check movies list query parameter pageSize was not set via wrong parameter pageLength"):
            assert (len(response_data["movies"])) == 10, "Wrong 'pageLength' filter was accepted for request"

        with allure.step("Check movies list query parameters locations, minPrice, maxPrice were not set via wrong parameter location, minimumPrice, maximumPrice"):
            for movie in response_data["movies"]:
                assert movie["location"] == 'MSK' or movie["location"] == 'SPB', "Wrong 'location' filter was accepted for request"
                assert 1 <= movie["price"] <= 1000000000, "Wrong 'minimumPrice' and 'maximumPrice' filters were accepted for request"

    @allure.feature("Testing of deleting movie")
    @allure.story("Validity of system behaviour when trying to delete non-existing movie")
    @allure.description("""
                        This test checks validity of system behaviour when trying to delete non-existing movie.
                        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Sergio Bagd")
    @allure.label("test_mood", "Negative")
    @allure.title("Test of trying to delete movie with non-existing ID")
    @pytest.mark.slow
    @pytest.mark.api
    @pytest.mark.negative
    def test_try_delete_non_existing_movie(self, super_admin, created_movie_for_deletion_test):
        nonexisting_movie_id = created_movie_for_deletion_test["id"] + 13

        with allure.step("Try to delete movie with non-existing ID and make sure status-code == 404"):
            response = super_admin.api.movies_api.delete_movie(nonexisting_movie_id, expected_status=404)
            response_data = response.json()

        with allure.step("Check there is a valid error message"):
            assert "message" in response_data
            assert response_data["message"] == "Фильм не найден", "Movie was found"

    @allure.feature("Testing of editing movie")
    @allure.story("Validity of system behaviour when trying to edit non-existing movie")
    @allure.description("""
                        This test checks validity of system behaviour when trying to edit non-existing movie.
                        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Sergio Bagd")
    @allure.label("test_mood", "Negative")
    @allure.title("Test of trying to edit movie with non-existing ID")
    @pytest.mark.api
    @pytest.mark.negative
    def test_try_edit_non_existing_movie(self, super_admin, created_movie):
        nonexisting_movie_id = created_movie["id"] + 13

        with allure.step("Try to edit movie with non-existing ID and make sure status-code == 404"):
            response = super_admin.api.movies_api.edit_movie(created_movie, nonexisting_movie_id, expected_status=404)
            response_data = response.json()

        with allure.step("Check there is a valid error message"):
            assert "message" in response_data
            assert response_data["message"] == "Фильм не найден", "Movie was found"

    @allure.feature("Testing of editing movie")
    @allure.story("Validity of system behaviour when trying to edit movie with wrong parameter")
    @allure.description("""
                        This test checks validity of system behaviour when trying to edit movie with wrong parameter.
                        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Sergio Bagd")
    @allure.label("test_mood", "Negative")
    @allure.title("Test of trying to edit movie with wrong parameter")
    @pytest.mark.api
    @pytest.mark.negative
    def test_try_edit_movie_with_wrong_parameter(self, super_admin, created_movie):
        edited_movie_data = {
            "title": created_movie["name"] + ' EDITED'
        }

        with allure.step("Try to edit movie with wrong parameter and make sure status-code == 404"):
            response = super_admin.api.movies_api.edit_movie(edited_movie_data, created_movie["id"], expected_status=404)
            response_data = response.json()

        with allure.step("Check there is a valid error message"):
            assert "message" in response_data
            assert response_data["message"] == "Фильм не найден", "Movie was found"

    @allure.feature("Testing of creating movie")
    @allure.story("Validity of system behaviour when trying to create movie by common user")
    @allure.description("""
                        This test checks validity of system behaviour when trying to create movie by common user. (user has no access to create movies)
                        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Sergio Bagd")
    @allure.label("test_mood", "Negative")
    @allure.title("Test of trying to create movie by common user")
    @pytest.mark.slow
    @pytest.mark.api
    @pytest.mark.negative
    def test_try_create_movie_by_common_user(self, common_user, test_movie):
        with allure.step("Try to create movie by common user and make sure status-code == 403"):
            response = common_user.api.movies_api.create_new_movie(test_movie, expected_status=403)
            response_data = response.json()

        with allure.step("Check there is a valid error message"):
            assert "message" in response_data
            assert response_data["message"] == "Forbidden resource", "Movie was created"

    @allure.feature("Testing of deleting movie")
    @allure.story("Validity of system behaviour when trying to delete movie by different users")
    @allure.description("""
                        This test checks validity of system behaviour when trying to delete movie by different users.
                        """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Sergio Bagd")
    @allure.title("Test of trying to delete movie by different users")
    @pytest.mark.parametrize("user_role,expected_status", [
        ("super_admin", 200),
        ("common_admin", 403),
        ("common_user", 403),
    ], ids = ["SuperAdmin", "Admin", "User"])
    @pytest.mark.slow
    @pytest.mark.api
    def test_delete_movie_by_different_roles(self, request, user_role, expected_status, created_movie_for_deletion_test):
        with allure.step("Delete movie by different roles and make sure status-code is expected"):
            user = request.getfixturevalue(user_role)
            user.api.movies_api.delete_movie(created_movie_for_deletion_test["id"], expected_status=expected_status)

    @allure.feature("Testing of creating movie")
    @allure.story("Validity of system behaviour when trying to create movie by different users")
    @allure.description("""
                            This test checks validity of system behaviour when trying to create movie by different users.
                            """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Sergio Bagd")
    @allure.title("Test of trying to create movie by different users")
    @pytest.mark.parametrize("user_role,expected_status", [
        ("super_admin", 201),
        ("common_admin", 403),
        ("common_user", 403),
    ], ids=["SuperAdmin", "Admin", "User"])
    @pytest.mark.db
    @pytest.mark.slow
    @pytest.mark.api
    def test_create_movie_by_different_roles(self, request, user_role, expected_status, test_movie, db_helper):
        with allure.step("Check if there is movie with same name in DB"):
            if db_helper.get_movie_by_name(test_movie["name"]) is not None:
                with allure.step("Change test_movie name to get rid of same names"):
                    test_movie["name"] = test_movie["name"] + DataGenerator.generate_random_movie_name()

        with allure.step("Create movie"):
            user = request.getfixturevalue(user_role)
        with allure.step("Create movie by different roles and make sure status-code is expected"):
            response = user.api.movies_api.create_new_movie(test_movie, expected_status=expected_status)
            response_data = response.json()
            if "id" in response_data:
                with allure.step("Check that movie was created in DB"):
                    assert db_helper.get_movie_by_id(response_data["id"]) is not None
            else:
                with allure.step("Check that movie was not created in DB"):
                    assert db_helper.get_movie_by_name(test_movie["name"]) is None









