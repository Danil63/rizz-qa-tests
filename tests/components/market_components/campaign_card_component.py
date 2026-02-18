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
