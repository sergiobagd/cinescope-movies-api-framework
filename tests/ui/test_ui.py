from playwright.sync_api import Page
from pages.register_page import CinescopeRegisterPage
from pages.login_page import CinescopeLoginPage
from pages.movie_page import CinescopeMoviePage
from utils.data_generator import DataGenerator
import allure
import pytest


@allure.epic("UI Testing")
@allure.feature("Testing Register Page")
@pytest.mark.ui
class TestRegisterPage:
    @allure.title("Successful registration by UI")
    @pytest.mark.positive
    def test_register_by_ui(self, page: Page):
        register_page = CinescopeRegisterPage(page)

        full_name = DataGenerator.generate_random_name()
        email = DataGenerator.generate_random_email()
        password = DataGenerator.generate_random_password()

        register_page.open()
        register_page.register(f"Playwright Test {full_name}", email, password)

        register_page.assert_was_redirect_to_login_page()

        register_page.make_screenshot_and_attach_to_allure("registerUI")

        register_page.assert_alert_was_popup()


@allure.epic("UI Testing")
@allure.feature("Testing Login Page")
@pytest.mark.ui
class TestLoginPage:
    @allure.title("Successful login by UI")
    @pytest.mark.positive
    def test_login_by_ui(self, page: Page, registered_user):
        login_page = CinescopeLoginPage(page)

        login_page.open()

        login_page.login(registered_user["email"], registered_user["password"])

        login_page.assert_was_redirect_to_home_page()

        login_page.make_screenshot_and_attach_to_allure("loginUI")

        login_page.assert_alert_was_pop_up()


@allure.epic("UI Testing")
@allure.feature("Testing Movie Page")
@pytest.mark.ui
class TestMoviePage:
    @allure.title("Successful adding review for movie by UI")
    @pytest.mark.positive
    def test_add_review_for_movie_by_ui(self, page: Page, logged_in_user_in_ui, created_movie, movie_review_params):

        movie_page = CinescopeMoviePage(page)

        movie_page.open_movie_page(created_movie["id"])

        movie_page.assert_movie_page(created_movie["name"])

        movie_page.add_review_for_movie(movie_review_params["review_text"], movie_review_params["review_rate"])

        movie_page.assert_review_appeared(movie_review_params["review_text"], movie_review_params["review_rate"])





