"""POM: Страница маркета блогера (creator market)."""
import allure
from playwright.sync_api import Page

from tests.pages.base_page import BasePage


class MarketPage(BasePage):
    """Page Object для https://app.rizz.market/app/creator/market."""

    URL = "https://app.rizz.market/app/creator/market"

    def __init__(self, page: Page):
        super().__init__(page)

    # ── Методы проверок ───────────────────────────────────────

    @allure.step('Checking creator market page is loaded')
    def expect_loaded(self) -> None:
        """Проверить что страница маркета блогера загружена."""
        self.expect_url_contains(r".*/app/creator/market")
