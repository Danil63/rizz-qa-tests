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
        self.details_heading = page.get_by_role("heading", name="Детали кампании")

        # ── Блок откликов (ссылка-карточка) ───────────────────
        self.responders_link = page.get_by_role("link", name="Отклики").first

        # ── Заголовок страницы откликов ───────────────────────
        self.offers_heading = page.get_by_role("heading", name="Отклики")

    def _blogger_card(self, username: str):
        """Найти listitem-карточку блогера по username."""
        return self.page.locator("li", has=self.page.locator("p", has_text=username))

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
        responders = self.page.locator(
            "div.text-xs.text-muted-foreground",
            has_text="количество откликнувшихся блогеров",
        )
        expect(responders).to_be_visible(timeout=10000)
        responders.click()

    @allure.step('Ожидание появления блогера "{username}" в списке откликов')
    def wait_for_blogger(self, username: str) -> None:
        blogger_username = self._blogger_card(username).locator("p", has_text=username)
        expect(blogger_username).to_be_visible(timeout=5000)

    @allure.step('Установить фокус на блогере "{username}"')
    def focus_blogger(self, username: str) -> None:
        self._blogger_card(username).locator(
            "p.flex.items-center.gap-2.truncate.text-slate-500", has_text=username
        ).focus()

    @allure.step('Нажать кнопку "Принять" у блогера "{username}"')
    def click_accept_for_blogger(self, username: str) -> None:
        card = self._blogger_card(username)
        accept_btn = card.get_by_role("button", name="Принять")
        expect(accept_btn).to_be_visible(timeout=10000)
        expect(accept_btn).to_be_enabled(timeout=10000)
        accept_btn.click()

    @allure.step('Ожидание исчезновения блогера "{username}" из списка')
    def wait_for_blogger_hidden(self, username: str) -> None:
        blogger_username = self._blogger_card(username).locator("p", has_text=username)
        expect(blogger_username).not_to_be_visible(timeout=15000)
