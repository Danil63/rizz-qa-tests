"""POM: Страница кампаний (campaigns)."""
from playwright.sync_api import Page

from tests.pages.base_page import BasePage


class CampaignsPage(BasePage):
    """Page Object для https://app.rizz.market/app/advertiser/campaigns."""

    URL = "https://app.rizz.market/app/advertiser/campaigns"

    def __init__(self, page: Page):
        super().__init__(page)

    # ── Проверки ──────────────────────────────────────────────

    def expect_loaded(self) -> None:
        """Проверить что страница кампаний загружена."""
        self.expect_url_contains(r".*/app/advertiser/campaigns")
        self.expect_heading("Кампании")
