from playwright.sync_api import Page, expect
from utils.data_generator import DataGenerator
import re
import allure


class PageAction:
    def __init__(self, page: Page):
        self.page = page

    @allure.step("Going to page: {url}")
    def open_url(self, url: str):
        self.page.goto(url)

    @allure.step("Entering text '{text}' in the field '{locator}'")
    def enter_text_to_elem(self, locator, text: str):
        locator.fill(text)

    @allure.step("Click element '{locator}'")
    def click_elem(self, locator):
        locator.click()

    @allure.step("Select option in locator '{locator}'")
    def select_option(self, locator, option):
        locator.click()
        self.page.get_by_role("option", name=f"{option}").click()

    @allure.step("Waiting for page to load: {url}")
    def wait_redirect_for_url(self, url: str):
        self.page.wait_for_url(url, timeout=5000)
        assert self.page.url == url

    @allure.step("Getting text of elem: '{locator}'")
    def get_elem_text(self, locator):
        locator.text_content()

    @allure.step("Wait for appearing or disappearing of elem: '{locator}', state = '{state}'")
    def wait_for_elem(self, locator, state):
        locator.wait_for(state=state)

    @allure.step("Screenshot of current page")
    def make_screenshot_and_attach_to_allure(self, test_name: str):
        screenshot_path = f"screenshot_{test_name}.png"
        self.page.screenshot(path=screenshot_path, full_page=True)

        # Attaching screenshot to allure report
        with open(screenshot_path, "rb") as file:
            allure.attach(file.read(), name="Screenshot after redirect", attachment_type=allure.attachment_type.PNG)

    @allure.step("Check pop up message with text: '{text}'")
    def check_pop_up_elem_with_text(self, text: str):
        with allure.step("Check pop up alert with text: '{text}'"):
            notification_locator = self.page.get_by_text(text)
            notification_locator.wait_for(state="visible")
            assert notification_locator.is_visible()

        with allure.step("Check disappearing of pop up with text: '{text}'"):
            notification_locator.wait_for(state="hidden")
            assert notification_locator.is_hidden()

class BasePage(PageAction):
    def __init__(self, page: Page):
        super().__init__(page)
        self.home_url = "https://dev-cinescope.coconutqa.ru/"

        # Mutual locators for every page on the website
        self.home_button = self.page.get_by_role("link", name="Cinescope")
        self.all_movies_button = self.page.get_by_role("link", name="Все фильмы")
        self.movie_details_button = self.page.locator("div").filter(has_text=re.compile(r"^Debra FullerCharge identify history study\.Подробнее$")).get_by_role("button")
        self.heading_text = self.page.get_by_role("heading", name="Последние фильмы")

    def open(self):
        self.open_url(self.home_url)

    @allure.step("Going to home page from website's header")
    def go_to_home_page(self):
        self.click_elem(self.home_button)
        self.wait_redirect_for_url(self.home_url)

    @allure.step("Going to all movies page from website's header")
    def go_to_all_movies_page(self):
        self.click_elem(self.all_movies_button)
        self.wait_redirect_for_url(f"{self.home_url}movies")

    def assert_home_page_heading(self):
        assert self.heading_text.text_content() == "Последние фильмы"

    def click_first_movie(self):
        self.click_elem(self.movie_details_button)


class CinescopeMoviePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # Locators of elems
        self.review_input = self.page.get_by_placeholder("Написать отзыв", exact=True)
        self.review_rate_selection_list = self.page.get_by_role("combobox")
        self.send_review_button = self.page.get_by_role("button", name="Отправить", exact=True)
        self.review_card = self.page.get_by_role("main")
        self.review_header = self.page.get_by_role("heading", name="Отзывы:")

        self.review_text = DataGenerator.generate_random_movie_description()
        self.review_rate = f"{DataGenerator.generate_random_movie_review_rate()}"

    def open(self):
        """Going to register page"""
        self.open_url(self.home_url)

    def assert_movie_page(self):
        self.wait_for_elem(self.review_header, state="visible")
        assert self.review_header.is_visible()
        assert self.review_header.text_content() == "Отзывы:"

    def add_review_for_movie(self):
        self.enter_text_to_elem(self.review_input, self.review_text)
        self.select_option(self.review_rate_selection_list, self.review_rate)
        self.click_elem(self.send_review_button)

    def assert_review_appeared(self):
        expect(self.review_card).to_contain_text(self.review_text)
        expect(self.review_card).to_contain_text(f"{self.review_rate}/5")

class CinescopeRegisterPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.home_url}register"

        # Locators of elems
        self.full_name_input = self.page.get_by_role("textbox", name="Имя Фамилия Отчество", exact=True)
        self.email_input = self.page.get_by_role("textbox", name="Email", exact=True)
        self.password_input = self.page.get_by_role("textbox", name="Пароль", exact=True)
        self.password_repeat_input = self.page.get_by_role("textbox", name="Повторите пароль", exact=True)

        self.register_button = self.page.get_by_role("button", name="Зарегистрироваться")
        self.sign_button = self.page.get_by_role("button", name="Войти")

    def open(self):
        """Going to register page"""
        self.open_url(self.url)

    def register(self, full_name: str, email: str, password: str):
        """Full registration process"""
        self.enter_text_to_elem(self.full_name_input, full_name)
        self.enter_text_to_elem(self.email_input, email)
        self.enter_text_to_elem(self.password_input, password)
        self.enter_text_to_elem(self.password_repeat_input, password)
        self.register_button.click()

    def assert_was_redirect_to_login_page(self):
        """Going to login page"""
        self.wait_redirect_for_url(f"{self.home_url}login")

    def assert_alert_was_popup(self):
        """Check alert pop up"""
        self.check_pop_up_elem_with_text("Подтвердите свою почту")

class CinescopeLoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.home_url}login"

        # Locators of elems
        self.email_input = self.page.get_by_role("textbox", name="Email", exact=True)
        self.password_input = self.page.get_by_role("textbox", name="Пароль", exact=True)

        self.login_button = self.page.locator("form").get_by_role("button", name="Войти")
        self.register_button = self.page.get_by_text("Зарегистрироваться")

    def open(self):
        self.open_url(self.url)

    def login(self, email, password):
        """Passing full login process"""
        self.enter_text_to_elem(self.email_input, email)
        self.enter_text_to_elem(self.password_input, password)
        self.login_button.click()

    def assert_was_redirect_to_home_page(self):
        """Ожидание перехода на домашнюю страницу"""
        self.wait_redirect_for_url(self.home_url)

    def assert_alert_was_pop_up(self):
        """Check alert pop up"""
        # Check pop up 'You logged in'
        self.check_pop_up_elem_with_text("Вы вошли в аккаунт")



