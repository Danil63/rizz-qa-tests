"""PCO: Компонент карточки кампании на маркете блогера."""
import allure
from playwright.sync_api import Page, Locator, expect

from tests.components.base_component import BaseComponent


class CampaignCardComponent(BaseComponent):
    """Первая карточка кампании на маркете — для проверки структуры."""

    def __init__(self, page: Page):
        super().__init__(page)

        # Первая карточка товара (по классу)
        self.card = page.locator(".rounded-xl.bg-white.p-1").first
        self.card_title = self.card.locator("h3")
        self.card_price_button = self.card.locator("button").first

        # ── Бейджи ────────────────────────────────────────────
        self.badge_auto_approve = self.card.locator("span.bg-purple")
        self.badge_tax_paid = self.card.locator("div.bg-lime", has_text="НАЛОГ ОПЛАЧЕН")
        self.badge_marking = self.card.locator("div.bg-lime", has_text="С МАРКИРОВКОЙ")

    # ── Методы проверок ───────────────────────────────────────

    @allure.step("Checking first campaign card is visible")
    def check_visible(self) -> None:
        """Проверить что первая карточка отображается."""
        expect(self.card).to_be_visible()
        expect(self.card_title).to_be_visible()

    @allure.step("Checking first campaign card has title text")
    def check_has_title(self) -> None:
        """Проверить что заголовок карточки не пустой."""
        text = self.card_title.text_content()
        assert text and len(text.strip()) > 0, "Заголовок карточки пустой"

    @allure.step("Checking first campaign card has price button")
    def check_has_price(self) -> None:
        """Проверить что у карточки есть кнопка с ценой/бартером."""
        expect(self.card_price_button).to_be_visible()

    @allure.step("Checking АВТООДОБРЕНИЕ badge in first card")
    def check_has_auto_approve(self) -> None:
        """Проверить что у карточки есть бейдж АВТООДОБРЕНИЕ."""
        expect(self.badge_auto_approve).to_be_visible()

    @allure.step("Checking НАЛОГ ОПЛАЧЕН badge in first card")
    def check_has_tax_paid(self) -> None:
        """Проверить что у карточки есть бейдж НАЛОГ ОПЛАЧЕН."""
        expect(self.badge_tax_paid).to_be_visible()

    @allure.step("Checking С МАРКИРОВКОЙ badge in first card")
    def check_has_marking(self) -> None:
        """Проверить что у карточки есть бейдж С МАРКИРОВКОЙ."""
        expect(self.badge_marking).to_be_visible()
