from playwright.sync_api import Page, expect
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
        return locator.text_content()

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

    @allure.step("Opening baseUrl: '{self.home_url}'")
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
