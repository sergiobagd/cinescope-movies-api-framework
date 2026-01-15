import requests
from constants import BASE_URL, REGISTER_ENDPOINT
import pytest
from utils.data_generator import DataGenerator
from custom_requester.custom_requester import CustomRequester
from clients.api_manager import ApiManager

@pytest.fixture(scope="session")
def session():
    """
    Fixture for creating an HTTP session
    """
    http_session = requests.Session()
    yield http_session
    http_session.close()



@pytest.fixture(scope="session")
def api_manager(session):
    """
    Fixture for creating an object of ApiManager
    """
    return ApiManager(session)

@pytest.fixture
def test_user():
    """
    Generation of a random user for tests
    """
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": ["USER"]
    }

@pytest.fixture
def registered_user(requester, test_user):
    """
    Фикстура для регистрации и получения данных зарегистрированного пользователя.
    """
    response = requester.send_request(
        method="POST",
        endpoint=REGISTER_ENDPOINT,
        data=test_user,
        expected_status=201
    )
    response_data = response.json()
    registered_user = test_user.copy()
    registered_user["id"] = response_data["id"]
    return registered_user

@pytest.fixture(scope="session")
def authenticated_super_admin_user(api_manager: ApiManager):
    """
    Fixture for authentication of super admin user.
    """
    credentials = ["api1@gmail.com", "asdqwe123Q"]
    response = api_manager.auth_api.authenticate(credentials)


@pytest.fixture(scope="session")
def requester():
    """
    Фикстура для создания экземпляра CustomRequester.
    """
    session = requests.Session()
    return CustomRequester(session=session, base_url=BASE_URL)
#
# @pytest.fixture(scope="session")
# def auth_session(test_user):
#     # Register a new user
#     register_url = f"{BASE_URL}{REGISTER_ENDPOINT}"
#     response = requests.post(register_url, json=test_user, headers=HEADERS)
#     assert response.status_code == 201, "Register error"
#
#     # Login for getting an accessToken
#     login_url = f"{BASE_URL}{LOGIN_ENDPOINT}"
#     login_data = {
#         "email": test_user["email"],
#         "password": test_user["password"]
#     }
#     response = requests.post(login_url, json=login_data, headers=HEADERS)
#     assert response.status_code == 200, "Login error"
#
#     # Getting accessToken and creating a session
#     token = response.json().get("accessToken")
#     assert token is not None, "accessToken is missing"
#
#     session = requests.Session()
#     session.headers.update(HEADERS)
#     session.headers.update({"Authorization": f"Bearer {token}"})
#     return session

@pytest.fixture
def test_user_different_password():
    """
    Generation of a random user for tests
    """
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password + "12",
        "roles": ["USER"]
    }

@pytest.fixture
def test_user_too_long_password():
    """
    Generation of a random user for tests
    """
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password + "100000002002303200002020200210200202",
        "passwordRepeat": random_password + "100000002002303200002020200210200202",
        "roles": ["USER"]
    }

@pytest.fixture
def test_user_not_allowed_symbols_password():
    """
    Generation of a random user for tests
    """
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password + "այբուբեն",
        "passwordRepeat": random_password + "այբուբեն",
        "roles": ["USER"]
    }

@pytest.fixture
def test_movie():
    """
    Generation of a random movie data for tests
    """
    random_movie_name = DataGenerator.generate_random_movie_name()
    random_image_url = DataGenerator.generate_random_movie_image_url()
    random_price = DataGenerator.generate_random_movie_price()
    random_description = DataGenerator.generate_random_movie_description()
    random_location = DataGenerator.generate_random_movie_location()
    random_genre_id = DataGenerator.generate_random_movie_genre_id()

    return {
        "name": random_movie_name,
        "imageUrl": random_image_url,
        "price": random_price,
        "description": random_description,
        "location": random_location,
        "published": True,
        "genreId": random_genre_id
    }

@pytest.fixture
def created_movie(api_manager: ApiManager, authenticated_super_admin_user, test_movie):
    response = api_manager.movies_api.create_new_movie(test_movie)
    movie = response.json()
    yield movie
    api_manager.movies_api.delete_movie(movie["id"])

@pytest.fixture
def created_movie_for_deletion_test(api_manager: ApiManager, authenticated_super_admin_user, test_movie):
    response = api_manager.movies_api.create_new_movie(test_movie)
    movie = response.json()
    yield movie

@pytest.fixture
def test_movie_non_existing_genre_id():
    """
    Generation of a random movie data for tests
    """
    random_movie_name = DataGenerator.generate_random_movie_name()
    random_image_url = DataGenerator.generate_random_movie_image_url()
    random_price = DataGenerator.generate_random_movie_price()
    random_description = DataGenerator.generate_random_movie_description()
    random_location = DataGenerator.generate_random_movie_location()
    random_genre_id = 109340909400034901

    return {
        "name": random_movie_name,
        "imageUrl": random_image_url,
        "price": random_price,
        "description": random_description,
        "location": random_location,
        "published": True,
        "genreId": random_genre_id
    }

@pytest.fixture
def test_movie_already_existing():
    """
    Generation of a random movie data for tests
    """
    existing_movie_name = "We."
    random_image_url = DataGenerator.generate_random_movie_image_url()
    random_price = DataGenerator.generate_random_movie_price()
    random_description = DataGenerator.generate_random_movie_description()
    random_location = DataGenerator.generate_random_movie_location()
    random_genre_id = DataGenerator.generate_random_movie_genre_id()

    return {
        "name": existing_movie_name,
        "imageUrl": random_image_url,
        "price": random_price,
        "description": random_description,
        "location": random_location,
        "published": True,
        "genreId": random_genre_id
    }

@pytest.fixture
def test_movie_empty_movie_name():
    """
    Generation of a random movie data for tests
    """
    empty_movie_name = ''
    random_image_url = DataGenerator.generate_random_movie_image_url()
    random_price = DataGenerator.generate_random_movie_price()
    random_description = DataGenerator.generate_random_movie_description()
    random_location = DataGenerator.generate_random_movie_location()
    random_genre_id = DataGenerator.generate_random_movie_genre_id()

    return {
        "name": empty_movie_name,
        "imageUrl": random_image_url,
        "price": random_price,
        "description": random_description,
        "location": random_location,
        "published": True,
        "genreId": random_genre_id
    }

@pytest.fixture
def test_movie_incorrect_movie_name_type():
    """
    Generation of a random movie data for tests
    """
    incorrect_movie_name = 1500
    random_image_url = DataGenerator.generate_random_movie_image_url()
    random_price = DataGenerator.generate_random_movie_price()
    random_description = DataGenerator.generate_random_movie_description()
    random_location = DataGenerator.generate_random_movie_location()
    random_genre_id = DataGenerator.generate_random_movie_genre_id()

    return {
        "name": incorrect_movie_name,
        "imageUrl": random_image_url,
        "price": random_price,
        "description": random_description,
        "location": random_location,
        "published": True,
        "genreId": random_genre_id
    }

@pytest.fixture
def test_movie_incorrect_price_type():
    """
    Generation of a random movie data for tests
    """
    random_movie_name = DataGenerator.generate_random_movie_name()
    random_image_url = DataGenerator.generate_random_movie_image_url()
    incorrect_price = "Heisenberg"
    random_description = DataGenerator.generate_random_movie_description()
    random_location = DataGenerator.generate_random_movie_location()
    random_genre_id = DataGenerator.generate_random_movie_genre_id()

    return {
        "name": random_movie_name,
        "imageUrl": random_image_url,
        "price": incorrect_price,
        "description": random_description,
        "location": random_location,
        "published": True,
        "genreId": random_genre_id
    }

@pytest.fixture
def test_movie_empty_location():
    """
    Generation of a random movie data for tests
    """
    random_movie_name = DataGenerator.generate_random_movie_name()
    random_image_url = DataGenerator.generate_random_movie_image_url()
    random_price = DataGenerator.generate_random_movie_price()
    random_description = DataGenerator.generate_random_movie_description()
    empty_location = ""
    random_genre_id = DataGenerator.generate_random_movie_genre_id()

    return {
        "name": random_movie_name,
        "imageUrl": random_image_url,
        "price": random_price,
        "description": random_description,
        "location": empty_location,
        "published": True,
        "genreId": random_genre_id
    }

@pytest.fixture
def test_movie_incorrect_imageUrl():
    """
    Generation of a random movie data for tests
    """
    random_movie_name = DataGenerator.generate_random_movie_name()
    incorrect_image_url = True
    random_price = DataGenerator.generate_random_movie_price()
    random_description = DataGenerator.generate_random_movie_description()
    random_location = DataGenerator.generate_random_movie_location()
    random_genre_id = DataGenerator.generate_random_movie_genre_id()

    return {
        "name": random_movie_name,
        "imageUrl": incorrect_image_url,
        "price": random_price,
        "description": random_description,
        "location": random_location,
        "published": True,
        "genreId": random_genre_id
    }

@pytest.fixture
def test_movie_incorrect_description():
    """
    Generation of a random movie data for tests
    """
    random_movie_name = DataGenerator.generate_random_movie_name()
    random_image_url = DataGenerator.generate_random_movie_image_url()
    random_price = DataGenerator.generate_random_movie_price()
    incorrect_description = 2026
    random_location = DataGenerator.generate_random_movie_location()
    random_genre_id = DataGenerator.generate_random_movie_genre_id()

    return {
        "name": random_movie_name,
        "imageUrl": random_image_url,
        "price": random_price,
        "description": incorrect_description,
        "location": random_location,
        "published": True,
        "genreId": random_genre_id
    }

@pytest.fixture
def test_movie_empty_published_status():
    """
    Generation of a random movie data for tests
    """
    random_movie_name = DataGenerator.generate_random_movie_name()
    random_image_url = DataGenerator.generate_random_movie_image_url()
    random_price = DataGenerator.generate_random_movie_price()
    random_description = DataGenerator.generate_random_movie_description()
    empty_published_status = None
    random_location = DataGenerator.generate_random_movie_location()
    random_genre_id = DataGenerator.generate_random_movie_genre_id()

    return {
        "name": random_movie_name,
        "imageUrl": random_image_url,
        "price": random_price,
        "description": random_description,
        "location": random_location,
        "published": empty_published_status,
        "genreId": random_genre_id
    }