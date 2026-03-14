"""POM: Лендинг rizz.market."""

from playwright.sync_api import Page

from tests.pages.base_page import BasePage


class LandingPage(BasePage):
    """Page Object для https://rizz.market/."""

    URL = "https://rizz.market/"

    def __init__(self, page: Page):
        super().__init__(page)

        # Локаторы элементов
        self.connect_button = page.get_by_text("Подключиться к платформе").first
        self.login_link = page.get_by_text("Вход").first

    # ── Методы действий ───────────────────────────────────────

    def open(self) -> None:
        """Открыть лендинг (тяжёлая страница)."""
        self.page.goto(self.URL, wait_until="commit", timeout=60000)
        self.connect_button.wait_for(state="visible", timeout=30000)

    def click_connect_button(self) -> None:
        """Нажать 'Подключиться к платформе'."""
        self.connect_button.click()
