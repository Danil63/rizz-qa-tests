"""POM: Детали кампании — обработка откликов блогеров."""

from playwright.sync_api import Page, expect

from tests.pages.base_page import BasePage


class CampaignDetailsPage(BasePage):
    """Page Object для страницы деталей кампании рекламодателя."""

    URL = "https://app.rizz.market/app/advertiser/campaigns"

    def __init__(self, page: Page):
        super().__init__(page)

        # ── Заголовок деталей (H3) ─────────────────────────────
        self.details_heading = page.locator("h3", has_text="Детали кампании")

        # ── Кнопка редактирования кампании ─────────────────────
        self.edit_button = page.get_by_role("link", name="Редактировать")

        # ── Ссылка на страницу откликов ────────────────────────
        self.responders_link = page.locator("a[href*='offers']").first

        # ── Заголовок страницы откликов (H2) ──────────────────
        self.offers_heading = page.locator("h2", has_text="Отклики")

    def _blogger_card(self, username: str):
        """Найти listitem-карточку блогера по username/display name."""
        return self.page.locator("li").filter(has_text=username)

    # ── Методы действий ───────────────────────────────────────

    def open(self) -> None:
        self.page.goto(self.URL, wait_until="domcontentloaded")
        self.page.wait_for_timeout(2000)

    def open_offers(self, campaign_id: str) -> None:
        url = f"https://app.rizz.market/app/advertiser/campaigns/{campaign_id}/offers"
        self.page.goto(url, wait_until="domcontentloaded")
        self.page.wait_for_timeout(3000)

    def click_edit_button(self) -> None:
        """Нажать кнопку перехода на страницу редактирования."""
        expect(self.edit_button).to_be_visible(timeout=10_000)
        self.edit_button.click()

    def click_campaign_title(self, campaign_title: str) -> None:
        campaign_el = self.page.get_by_text(campaign_title, exact=True).first
        expect(campaign_el).to_be_visible(timeout=15000)
        campaign_el.click()
        self.page.wait_for_timeout(3000)

    def wait_for_details_heading(self) -> None:
        expect(self.details_heading).to_be_visible(timeout=10000)

    def click_offers_link(self) -> None:
        expect(self.responders_link).to_be_visible(timeout=10000)
        self.responders_link.click()
        self.page.wait_for_timeout(2000)

    def wait_for_offers_heading(self) -> None:
        expect(self.offers_heading).to_be_visible(timeout=10000)

    def click_responders_count(self) -> None:
        responders = self.page.locator(
            "div.text-xs.text-muted-foreground",
            has_text="количество откликнувшихся блогеров",
        )
        expect(responders).to_be_visible(timeout=10000)
        responders.click()

    def wait_for_blogger(self, username: str) -> None:
        card = self._blogger_card(username)
        expect(card).to_be_visible(timeout=15000)

    def focus_blogger(self, username: str) -> None:
        self._blogger_card(username).hover()

    def click_accept_for_blogger(self, username: str) -> None:
        card = self._blogger_card(username)
        accept_btn = card.get_by_role("button", name="Принять")
        expect(accept_btn).to_be_visible(timeout=10000)
        expect(accept_btn).to_be_enabled(timeout=10000)
        accept_btn.click()

    def wait_for_blogger_hidden(self, username: str) -> None:
        expect(self._blogger_card(username)).not_to_be_visible(timeout=5000)
