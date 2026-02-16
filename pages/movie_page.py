from playwright.sync_api import Page, expect
import allure
from pages.base_page import BasePage

class CinescopeMoviePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # Locators of elems
        self.review_input = self.page.get_by_placeholder("Написать отзыв", exact=True)
        self.review_rate_selection_list = self.page.get_by_role("combobox")
        self.send_review_button = self.page.get_by_role("button", name="Отправить", exact=True)
        self.review_card = self.page.get_by_role("main")
        self.review_header = self.page.get_by_role("heading", name="Отзывы:")

    @allure.step("Opening movie page")
    def open_movie_page(self, movie_id):
        """Going to movie page"""
        self.open_url(f"{self.home_url}movies/{movie_id}")

    @allure.step("Asserting movie page by visibility of movie name and reviews")
    def assert_movie_page(self, movie_name):
        self.wait_for_elem(self.review_header, state="visible")
        assert self.page.get_by_text(f"{movie_name}").is_visible()
        assert self.review_header.is_visible()
        assert self.review_header.text_content() == "Отзывы:"

    @allure.step("Filling review inputs and post review about movie")
    def add_review_for_movie(self, review_text, review_rate):
        self.enter_text_to_elem(self.review_input, review_text)
        self.select_option(self.review_rate_selection_list, review_rate)
        self.click_elem(self.send_review_button)

    @allure.step("Asserting that review appeared on the movie page")
    def assert_review_appeared(self, review_text, review_rate):
        expect(self.review_card).to_contain_text(review_text)
        expect(self.review_card).to_contain_text(f"{review_rate}/5")
