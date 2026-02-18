"""POM: Лендинг rizz.market."""
import allure
from playwright.sync_api import Page

from tests.pages.base_page import BasePage


class LandingPage(BasePage):
    """Page Object для https://rizz.market/."""

    URL = "https://rizz.market/"

    def __init__(self, page: Page):
        super().__init__(page)

        # Локаторы элементов
        self.connect_button = page.get_by_text("Подключиться к платформе").first

    # ── Методы действий ───────────────────────────────────────

    @allure.step('Clicking "Подключиться к платформе" button')
    def click_connect_button(self) -> None:
        """Нажать 'Подключиться к платформе'."""
        self.connect_button.click()
