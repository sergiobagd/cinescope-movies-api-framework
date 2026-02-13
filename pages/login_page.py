from playwright.sync_api import Page, expect
import allure
from pages.base_page import BasePage


class CinescopeLoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.home_url}login"

        # Locators of elems
        self.email_input = self.page.get_by_role("textbox", name="Email", exact=True)
        self.password_input = self.page.get_by_role("textbox", name="Пароль", exact=True)

        self.login_button = self.page.locator("form").get_by_role("button", name="Войти")
        self.register_button = self.page.get_by_text("Зарегистрироваться")

    @allure.step("Opening login page")
    def open(self):
        """Going to login page"""
        self.open_url(self.url)

    @allure.step("Filling all login inputs and log in user")
    def login(self, email, password):
        """Passing full login process"""
        self.enter_text_to_elem(self.email_input, email)
        self.enter_text_to_elem(self.password_input, password)
        self.login_button.click()

    @allure.step("Asserting successful redirect to home page")
    def assert_was_redirect_to_home_page(self):
        """Ожидание перехода на домашнюю страницу"""
        self.wait_redirect_for_url(self.home_url)

    @allure.step("Asserting visibility of successful logging in pop-up")
    def assert_alert_was_pop_up(self):
        """Check alert pop up"""
        # Check pop up 'You logged in'
        self.check_pop_up_elem_with_text("Вы вошли в аккаунт")
