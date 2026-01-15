from clients.api_manager import ApiManager

class TestMoviesAPI:
    def test_get_movies_list(self, api_manager: ApiManager):
        response = api_manager.movies_api.get_movies_list()
        response_data = response.json()

        assert response.status_code == 200
        assert response_data["movies"] is not None

    def test_get_movies_list_by_filters(self, api_manager: ApiManager):
        response = api_manager.movies_api.get_movies_list_by_filters()
        response_data = response.json()

        assert response.status_code == 200
        assert response_data["movies"] is not None
        assert (len(response_data["movies"])) == 10
        for movie in response_data["movies"]:
            assert movie["location"] == 'MSK'
            assert 1 <= movie["price"] <= 500

    def test_create_movie(self, api_manager: ApiManager, authenticated_super_admin_user, test_movie):

        response = api_manager.movies_api.create_new_movie(test_movie)
        response_data = response.json()

        assert response.status_code == 201
        assert response_data["id"] is not None

    def test_get_specific_movie(self, api_manager: ApiManager, created_movie):
        response = api_manager.movies_api.get_specific_movie(created_movie["id"])
        response_data = response.json()

        assert response.status_code == 200
        assert created_movie["id"] == response_data["id"]
        assert created_movie["name"] == response_data["name"]

    def test_edit_movie(self, api_manager: ApiManager, created_movie):
        response = api_manager.movies_api.edit_movie(created_movie, created_movie["id"])
        response_data = response.json()

        assert response.status_code == 200
        assert response_data["name"] != created_movie["name"]
        assert response_data["name"] == created_movie["name"] + ' EDITED'

    def test_delete_movie(self, api_manager: ApiManager, created_movie_for_deletion_test):
        response = api_manager.movies_api.delete_movie(created_movie_for_deletion_test["id"])
        response_data = response.json()

        assert response.status_code == 200
        assert created_movie_for_deletion_test["id"] == response_data["id"]

        response_get_deleted_movie = api_manager.movies_api.get_specific_movie(response_data["id"], expected_status = 404)
        assert response_get_deleted_movie.status_code == 404

    def test_try_create_movie_already_existing(self, api_manager: ApiManager, authenticated_super_admin_user, test_movie_already_existing):
        response = api_manager.movies_api.create_new_movie(test_movie_already_existing, expected_status = 409)
        response_data = response.json()

        assert response.status_code == 409
        assert "id" not in response_data
        assert response_data["message"] == "Фильм с таким названием уже существует", "Already existing movie was created"

    def test_try_create_movie_with_non_existing_genre_id(self, api_manager: ApiManager, authenticated_super_admin_user, test_movie_non_existing_genre_id):
        response = api_manager.movies_api.create_new_movie(test_movie_non_existing_genre_id, expected_status = 400)
        response_data = response.json()

        assert response.status_code == 400
        assert "id" not in response_data
        assert response_data["message"] == "Некорректные данные", "Non existing genreId was accepted"

    def test_try_create_movie_with_empty_name(self, api_manager: ApiManager, authenticated_super_admin_user, test_movie_empty_movie_name):
        response = api_manager.movies_api.create_new_movie(test_movie_empty_movie_name, expected_status = 400)
        response_data = response.json()

        assert response.status_code == 400
        assert "id" not in response_data
        assert response_data["message"] == ["name should not be empty"], "Empty name was accepted"

    def test_try_create_movie_with_incorrect_name_type(self, api_manager: ApiManager, authenticated_super_admin_user, test_movie_incorrect_movie_name_type):
        response = api_manager.movies_api.create_new_movie(test_movie_incorrect_movie_name_type, expected_status = 400)
        response_data = response.json()

        assert response.status_code == 400
        assert "id" not in response_data
        assert response_data["message"] == ["Поле name должно быть строкой"], "Incorrect name was accepted"

    def test_try_create_movie_with_incorrect_price_type(self, api_manager: ApiManager, authenticated_super_admin_user, test_movie_incorrect_price_type):
        response = api_manager.movies_api.create_new_movie(test_movie_incorrect_price_type, expected_status=400)
        response_data = response.json()

        assert response.status_code == 400
        assert "id" not in response_data
        assert response_data["message"] == ["Поле price должно быть числом"], "Incorrect price was accepted"

    def test_try_create_movie_with_empty_location(self, api_manager: ApiManager, authenticated_super_admin_user, test_movie_empty_location):
        response = api_manager.movies_api.create_new_movie(test_movie_empty_location, expected_status=400)
        response_data = response.json()

        assert response.status_code == 400
        assert "id" not in response_data
        assert response_data["message"] == ["Поле location должно быть одним из: MSK, SPB"], "Empty location was accepted"


    def test_try_create_movie_with_incorrect_imageUrl(self, api_manager: ApiManager, authenticated_super_admin_user, test_movie_incorrect_imageUrl):
        response = api_manager.movies_api.create_new_movie(test_movie_incorrect_imageUrl, expected_status=400)
        response_data = response.json()

        assert response.status_code == 400
        assert "id" not in response_data
        assert response_data["message"] == [
        "Неверная ссылка",
        "Поле imageUrl должно быть строкой"], "Incorrect imageUrl was accepted"

    def test_try_create_movie_with_incorrect_description(self, api_manager: ApiManager, authenticated_super_admin_user, test_movie_incorrect_description):
        response = api_manager.movies_api.create_new_movie(test_movie_incorrect_description, expected_status=400)
        response_data = response.json()

        assert response.status_code == 400
        assert "id" not in response_data
        assert response_data["message"] == ["Поле description должно быть строкой"], "Wrong description was accepted"

    def test_try_create_movie_with_empty_published_status(self, api_manager: ApiManager, authenticated_super_admin_user, test_movie_empty_published_status):
        response = api_manager.movies_api.create_new_movie(test_movie_empty_published_status, expected_status=400)
        response_data = response.json()

        assert response.status_code == 400
        assert "id" not in response_data
        assert response_data["message"] == ["Поле published должно быть булевым значением"], "Empty published status was accepted"

    def test_try_get_specific_non_existing_movie(self, api_manager: ApiManager):
        nonexisting_movie_id = 0
        response = api_manager.movies_api.get_specific_movie(nonexisting_movie_id, expected_status=404)
        response_data = response.json()

        assert response.status_code == 404
        assert nonexisting_movie_id not in response_data, "Non existing movie was found"
        assert response_data["message"] == "Фильм не найден", "Movie was found"

    def test_try_get_movies_list_with_wrong_filters(self, api_manager: ApiManager):
        response = api_manager.movies_api.get_movies_list_by_wrong_filters()
        response_data = response.json()

        assert response.status_code == 200
        assert response_data["movies"] is not None
        assert (len(response_data["movies"])) == 10, "Wrong 'pageLength' filter was accepted for request"
        for movie in response_data["movies"]:
            assert movie["location"] == 'MSK' or movie["location"] == 'SPB', "Wrong 'location' filter was accepted for request"
            assert 1 <= movie["price"] <= 1000000000, "Wrong 'minimumPrice' and 'maximumPrice' filters were accepted for request"

    def test_try_delete_non_existing_movie(self, api_manager: ApiManager, created_movie_for_deletion_test):
        nonexisting_movie_id = created_movie_for_deletion_test["id"]+13
        response = api_manager.movies_api.delete_movie(nonexisting_movie_id, expected_status=404)
        response_data = response.json()

        assert response.status_code == 404, "Non-existing movie was deleted"
        assert response_data["message"] == "Фильм не найден", "Movie was found"

    def test_try_edit_non_existing_movie(self, api_manager: ApiManager, created_movie):
        nonexisting_movie_id = created_movie["id"] + 13
        response = api_manager.movies_api.edit_movie(created_movie, nonexisting_movie_id, expected_status=404)

        assert response.status_code == 404, "Movie was edited"

    def test_try_edit__movie_with_wrong_parameter(self, api_manager: ApiManager, created_movie):
        response = api_manager.movies_api.edit_movie_with_wrong_parameter(created_movie, created_movie["id"])

        assert response.status_code == 404, "Movie was edited"





