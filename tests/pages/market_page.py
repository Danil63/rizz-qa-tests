"""POM: Страница маркета блогера (creator market)."""
import allure
from playwright.sync_api import Page, expect

from tests.pages.base_page import BasePage
from tests.components.market.campaign_card_component import CampaignCardComponent


class MarketPage(BasePage):
    """Page Object для https://app.rizz.market/app/creator/market."""

    URL = "https://app.rizz.market/app/creator/market"

    def __init__(self, page: Page):
        super().__init__(page)

        # ── Компоненты ────────────────────────────────────────
        self.first_card = CampaignCardComponent(page)

        # ── Хедер (навигация) ─────────────────────────────────
        self.logo_link = page.get_by_role("banner").get_by_role("link").first
        self.nav_market = page.get_by_role("navigation").get_by_role("link", name="Маркет")
        self.nav_offers = page.get_by_role("navigation").get_by_role("link", name="Отклики")
        self.nav_integrations = page.get_by_role("navigation").get_by_role("link", name="Интеграции")
        self.nav_faq = page.get_by_role("navigation").get_by_role("link", name="FAQ")
        self.user_avatar_button = page.get_by_role("button", name="user avatar")

        # ── Уведомление Telegram ──────────────────────────────
        self.telegram_notification = page.get_by_text("Подключите уведомления в Telegram")

        # ── Сторис ────────────────────────────────────────────
        self.stories_buttons = page.locator("button[class*='stories-card'], button[id*='stories-card']")

        # ── Баннер-карусель ───────────────────────────────────
        self.carousel_prev = page.get_by_role("button", name="Previous slide")
        self.carousel_next = page.get_by_role("button", name="Next slide")

        # ── Поиск ─────────────────────────────────────────────
        self.search_input = page.get_by_role("textbox", name="Поиск")

        # ── Фильтры ──────────────────────────────────────────
        self.filter_social = page.get_by_role("button", name="Социальная сеть")
        self.filter_marketplace = page.get_by_role("button", name="Маркетплейс")
        self.filter_category = page.get_by_role("button", name="Категория")
        self.filter_reward = page.get_by_role("button", name="Вознаграждение")
        self.filter_options = page.get_by_role("button", name="Опции кампании")
        self.filter_sort = page.get_by_role("button", name="Сортировка")

        # ── Реферальный баннер ────────────────────────────────
        self.referral_banner = page.get_by_text("НАЖМИ И ПОЛУЧИ 600 РУБЛЕЙ")
        self.referral_get_button = page.get_by_role("link", name="Получить")

        # ── Пагинация ────────────────────────────────────────
        self.load_more_button = page.get_by_role("button", name="Загрузить ещё")
        self.all_loaded_alert = page.get_by_text("Это все предложения для вас на данный момент.")

        # ── Футер ─────────────────────────────────────────────
        self.footer_copyright = page.get_by_text('ООО "Трафик агрегатор"')
        self.footer_about_link = page.get_by_role("link", name="О нас")

        # ── Cookie-диалог ─────────────────────────────────────
        self.cookie_dialog = page.get_by_role("dialog", name="Согласие на cookie")
        self.cookie_accept = page.get_by_role("button", name="Принять cookie")
        self.cookie_decline = page.get_by_role("button", name="Отказаться")

    # ── Методы действий ───────────────────────────────────────

    @allure.step('Accepting cookie consent')
    def accept_cookies(self) -> None:
        """Принять cookie, если диалог отображается."""
        if self.cookie_accept.is_visible(timeout=3000):
            self.cookie_accept.click()

    @allure.step('Clicking "Загрузить ещё" button')
    def click_load_more(self) -> None:
        """Нажать 'Загрузить ещё'."""
        self.load_more_button.click()

    @allure.step('Typing "{query}" in search field')
    def search(self, query: str) -> None:
        """Ввести текст в поле поиска."""
        self.search_input.click()
        self.search_input.fill(query)

    @allure.step('Clicking carousel next slide')
    def click_next_slide(self) -> None:
        """Нажать следующий слайд карусели."""
        self.carousel_next.click()

    @allure.step('Clicking carousel previous slide')
    def click_prev_slide(self) -> None:
        """Нажать предыдущий слайд карусели."""
        self.carousel_prev.click()

    # ── Методы проверок ───────────────────────────────────────

    @allure.step('Checking creator market page is loaded')
    def expect_loaded(self) -> None:
        """Проверить что страница маркета блогера загружена."""
        self.expect_url_contains(r".*/app/creator/market")

    @allure.step('Checking header navigation is visible')
    def check_navigation_visible(self) -> None:
        """Проверить видимость навигации в хедере."""
        expect(self.nav_market).to_be_visible()
        expect(self.nav_offers).to_be_visible()
        expect(self.nav_integrations).to_be_visible()
        expect(self.nav_faq).to_be_visible()

    @allure.step('Checking user avatar button is visible')
    def check_user_avatar_visible(self) -> None:
        """Проверить видимость кнопки аватара пользователя."""
        expect(self.user_avatar_button).to_be_visible()

    @allure.step('Checking search input is visible')
    def check_search_visible(self) -> None:
        """Проверить видимость поля поиска."""
        expect(self.search_input).to_be_visible()

    @allure.step('Checking all filter buttons are visible')
    def check_filters_visible(self) -> None:
        """Проверить видимость всех кнопок фильтров."""
        expect(self.filter_social).to_be_visible()
        expect(self.filter_marketplace).to_be_visible()
        expect(self.filter_category).to_be_visible()
        expect(self.filter_reward).to_be_visible()
        expect(self.filter_options).to_be_visible()
        expect(self.filter_sort).to_be_visible()

    @allure.step('Checking carousel controls are visible')
    def check_carousel_visible(self) -> None:
        """Проверить видимость кнопок карусели."""
        expect(self.carousel_prev).to_be_visible()
        expect(self.carousel_next).to_be_visible()

    @allure.step('Checking referral banner is visible')
    def check_referral_banner_visible(self) -> None:
        """Проверить видимость реферального баннера."""
        expect(self.referral_banner).to_be_visible()

    @allure.step('Checking footer is visible')
    def check_footer_visible(self) -> None:
        """Проверить видимость футера."""
        expect(self.footer_copyright).to_be_visible()
        expect(self.footer_about_link).to_be_visible()
