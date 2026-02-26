"""POM: Детали кампании — обработка откликов блогеров."""
import allure
from playwright.sync_api import Page, expect

from tests.pages.base_page import BasePage


class CampaignDetailsPage(BasePage):
    """Page Object для страницы деталей кампании рекламодателя."""

    URL = "https://app.rizz.market/app/advertiser/campaigns"

    def __init__(self, page: Page):
        super().__init__(page)

        # ── Заголовок деталей ─────────────────────────────────
        self.details_heading = page.locator(
            "h3.text-xl.font-semibold.leading-none.tracking-tight",
            has_text="Детали кампании",
        )

        # ── Блок откликов ─────────────────────────────────────
        self.responders_count = page.locator(
            "div.text-xs.text-muted-foreground",
            has_text="количество откликнувшихся блогеров",
        )

        # ── Блогер danil23319 ─────────────────────────────────
        self.blogger_danil = page.locator(
            "p.flex.items-center.gap-2.truncate.text-slate-500",
            has_text="danil23319",
        )

        # ── Кнопка Принять ────────────────────────────────────
        self.accept_button = page.get_by_role("button", name="Принять").first

    # ── Методы действий ───────────────────────────────────────

    @allure.step('Открыть страницу кампаний')
    def open(self) -> None:
        self.page.goto(self.URL, wait_until="networkidle")

    @allure.step('Нажать на заголовок кампании "{campaign_title}"')
    def click_campaign_title(self, campaign_title: str) -> None:
        campaign_el = self.page.get_by_text(campaign_title, exact=True).first
        expect(campaign_el).to_be_visible(timeout=15000)
        campaign_el.click()

    @allure.step('Ожидание заголовка "Детали кампании" (3000 мс)')
    def wait_for_details_heading(self) -> None:
        self.page.wait_for_timeout(3000)
        expect(self.details_heading).to_be_visible(timeout=10000)

    @allure.step('Нажать на "количество откликнувшихся блогеров"')
    def click_responders_count(self) -> None:
        expect(self.responders_count).to_be_visible(timeout=10000)
        self.responders_count.click()

    @allure.step('Ожидание появления блогера "danil23319"')
    def wait_for_blogger_danil(self) -> None:
        expect(self.blogger_danil).to_be_visible(timeout=5000)

    @allure.step('Установить фокус на "danil23319"')
    def focus_blogger_danil(self) -> None:
        self.blogger_danil.focus()

    @allure.step('Нажать кнопку "Принять"')
    def click_accept(self) -> None:
        expect(self.accept_button).to_be_visible(timeout=10000)
        expect(self.accept_button).to_be_enabled(timeout=10000)
        self.accept_button.click()

    @allure.step('Ожидание исчезновения "danil23319"')
    def wait_for_blogger_danil_hidden(self) -> None:
        expect(self.blogger_danil).not_to_be_visible(timeout=15000)
