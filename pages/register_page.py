from playwright.sync_api import Page, expect
import allure
from base_page import BasePage

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

    @allure.step("Opening register page")
    def open(self):
        """Going to register page"""
        self.open_url(self.url)

    @allure.step("Filling all register inputs and register user")
    def register(self, full_name: str, email: str, password: str):
        """Full registration process"""
        self.enter_text_to_elem(self.full_name_input, full_name)
        self.enter_text_to_elem(self.email_input, email)
        self.enter_text_to_elem(self.password_input, password)
        self.enter_text_to_elem(self.password_repeat_input, password)
        self.register_button.click()

    @allure.step("Asserting successful redirect to login page")
    def assert_was_redirect_to_login_page(self):
        """Going to login page"""
        self.wait_redirect_for_url(f"{self.home_url}login")

    @allure.step("Asserting visibility of confirming email pop-up")
    def assert_alert_was_popup(self):
        """Check alert pop up"""
        self.check_pop_up_elem_with_text("Подтвердите свою почту")
