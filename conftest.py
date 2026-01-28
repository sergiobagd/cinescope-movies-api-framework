import requests
from constants.roles import Roles
import pytest
from utils.data_generator import DataGenerator
from clients.api_manager import ApiManager
from entities.user import User
from resources.user_creds import SuperAdminCreds
from constants.models import TestUser


@pytest.fixture(scope="session")
def session():
    """
    Fixture for creating an HTTP session
    """
    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()

@pytest.fixture
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        [Roles.SUPER_ADMIN.value],
        new_session
    )

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin

@pytest.fixture(scope="session")
def api_manager(session):
    """
    Fixture for creating an object of ApiManager
    """
    return ApiManager(session)

@pytest.fixture
def test_user() -> TestUser:
    """
    Generation of a random user for tests
    """
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return TestUser(
        email=random_email,
        fullName=random_name,
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER]
    )

@pytest.fixture
def creation_user_data(test_user):
    updated_user = test_user
    updated_user.verified = True
    updated_user.banned = False

    return updated_user

@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    common_user = User(
        creation_user_data.email,
        creation_user_data.password,
        [Roles.USER.value],
        new_session)

    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user

@pytest.fixture
def common_admin(user_session, super_admin, creation_user_data):
    new_session = user_session()

    common_admin = User(
        creation_user_data.email,
        creation_user_data.password,
        [Roles.ADMIN.value],
        new_session
    )

    new_roles = {
        "roles": [Roles.USER.value, Roles.ADMIN.value]
    }
    response = super_admin.api.user_api.create_user(creation_user_data).json()
    super_admin.api.user_api.update_user(new_roles, response["id"])
    common_admin.api.auth_api.authenticate(common_admin.creds)
    return common_admin

@pytest.fixture
def registered_user(api_manager: ApiManager, test_user):
    """
    Fixture for registration of user and getting its info.
    """
    api_manager.auth_api.register_user(test_user)
    registered_user_creds = {
        "email": test_user.email,
        "password": test_user.password
    }
    return registered_user_creds

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
def created_movie(super_admin, test_movie):
    response = super_admin.api.movies_api.create_new_movie(test_movie)
    movie = response.json()
    yield movie
    super_admin.api.movies_api.delete_movie(movie["id"])

@pytest.fixture
def created_movie_for_deletion_test(super_admin, test_movie):
    response = super_admin.api.movies_api.create_new_movie(test_movie)
    movie = response.json()
    yield movie

