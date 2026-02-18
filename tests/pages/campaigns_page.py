"""POM: Страница списка рекламных кампаний рекламодателя."""
import allure
from playwright.sync_api import Page, expect

from tests.pages.base_page import BasePage


class CampaignsPage(BasePage):
    """Page Object для https://app.rizz.market/app/advertiser/campaigns."""

    URL = "https://app.rizz.market/app/advertiser/campaigns"

    def __init__(self, page: Page):
        super().__init__(page)

        # ── Хедер (навигация рекламодателя) ───────────────────
        self.logo_link = page.get_by_role("banner").get_by_role("link").first
        self.nav_market = page.get_by_role("navigation").get_by_role("link", name="Маркет")
        self.nav_campaigns = page.get_by_role("navigation").get_by_role("link", name="Кампании")
        self.nav_products = page.get_by_role("navigation").get_by_role("link", name="Продукты")
        self.nav_integrations = page.get_by_role("navigation").get_by_role("link", name="Интеграции")
        self.nav_statistics = page.get_by_role("navigation").get_by_role("link", name="Статистика")
        self.nav_faq = page.get_by_role("navigation").get_by_role("link", name="FAQ")
        self.notification_bell = page.get_by_role("banner").get_by_role("button").first
        self.user_avatar_button = page.get_by_role("button", name="user avatar")

        # ── Уведомление Telegram ──────────────────────────────
        self.telegram_notification = page.get_by_text(
            "Подключите уведомления в Telegram"
        )
        self.telegram_close_button = page.locator(
            "button:near(:text('Подключите уведомления в Telegram'))"
        ).last

        # ── Баннер-карусель ───────────────────────────────────
        self.carousel_region = page.get_by_role("region").first
        self.carousel_prev = page.get_by_role("button", name="Previous slide")
        self.carousel_next = page.get_by_role("button", name="Next slide")

        # ── Заголовок и описание ──────────────────────────────
        self.heading = page.get_by_role("heading", name="Кампании")
        self.description = page.get_by_text("Список ваших рекламных кампаний.")
        self.how_it_works_button = page.get_by_role("button", name="Как это работает?")

        # ── Кнопка создания кампании ──────────────────────────
        self.create_link = page.get_by_role("link", name="Создать")

        # ── Фильтр ведения (combobox) ────────────────────────
        self.filter_management = page.get_by_role("combobox").first

        # ── Сортировка ────────────────────────────────────────
        self.sort_button = page.get_by_role("button", name="Сначала новые")

        # ── Табы статусов ─────────────────────────────────────
        self.tab_active = page.get_by_role("radio", name="Активные")
        self.tab_paused = page.get_by_role("radio", name="Приостановленные")
        self.tab_completed = page.get_by_role("radio", name="Завершенные")
        self.tab_all = page.get_by_role("radio", name="Все")

        # ── Список кампаний ───────────────────────────────────
        self.campaign_items = page.get_by_role("listitem")
        self.first_campaign = page.get_by_role("listitem").first
        self.first_campaign_image = self.first_campaign.locator("img").first
        self.first_campaign_link = self.first_campaign.get_by_role("link").first
        self.first_campaign_menu = self.first_campaign.get_by_role("button")

        # ── Бейджи первой кампании ────────────────────────────
        self.first_campaign_status_badge = self.first_campaign.locator(
            ".rounded-full.border", has_text="Активна"
        )
        self.first_campaign_management_badge = self.first_campaign.locator(
            ".rounded-full.border", has_text="На ведении"
        )

        # ── Данные первой кампании (dt/dd) ────────────────────
        self.first_campaign_offers = self.first_campaign.locator("dt", has_text="Отклики")
        self.first_campaign_integrations = self.first_campaign.locator("dt", has_text="Интеграции")
        self.first_campaign_cost = self.first_campaign.locator("dt", has_text="Стоимость")
        self.first_campaign_reward = self.first_campaign.locator(
            "dt", has_text="Вознаграждение"
        )

        # ── Футер ─────────────────────────────────────────────
        self.footer_copyright = page.get_by_text('ООО "Трафик агрегатор"')
        self.footer_about_link = page.get_by_role("link", name="О нас")

        # ── Cookie-диалог ─────────────────────────────────────
        self.cookie_accept = page.get_by_role("button", name="Принять cookie")
        self.cookie_decline = page.get_by_role("button", name="Отказаться")

    # ── Методы действий ───────────────────────────────────────

    @allure.step("Принять cookie")
    def accept_cookies(self) -> None:
        """Принять cookie, если диалог отображается."""
        if self.cookie_accept.is_visible(timeout=3000):
            self.cookie_accept.click()

    @allure.step("Клик по кнопке Создать")
    def click_create(self) -> None:
        """Нажать кнопку Создать кампанию."""
        self.create_link.click()

    @allure.step('Переключение на таб "{tab_name}"')
    def switch_tab(self, tab_name: str) -> None:
        """Переключить таб статуса: Активные, Приостановленные, Завершенные, Все."""
        mapping = {
            "Активные": self.tab_active,
            "Приостановленные": self.tab_paused,
            "Завершенные": self.tab_completed,
            "Все": self.tab_all,
        }
        mapping[tab_name].click()

    @allure.step('Выбор фильтра ведения: "{option}"')
    def select_management_filter(self, option: str) -> None:
        """Выбрать фильтр ведения: Все, На ведении, Самостоятельно."""
        self.filter_management.click()
        self.page.get_by_role("option", name=option, exact=True).click()

    @allure.step('Выбор сортировки: "{option}"')
    def select_sort(self, option: str) -> None:
        """Выбрать сортировку: Сначала новые, Сначала старые."""
        self.sort_button.click()
        self.page.get_by_role("option", name=option).click()

    @allure.step("Клик по первой кампании")
    def click_first_campaign(self) -> None:
        """Перейти в первую кампанию из списка."""
        self.first_campaign_link.click()

    @allure.step("Клик по карусели — следующий слайд")
    def click_next_slide(self) -> None:
        """Нажать следующий слайд карусели."""
        self.carousel_next.click()

    @allure.step("Клик по карусели — предыдущий слайд")
    def click_prev_slide(self) -> None:
        """Нажать предыдущий слайд карусели."""
        self.carousel_prev.click()

    # ── Методы получения данных ────────────────────────────────

    @allure.step("Получение названия первой кампании")
    def get_first_campaign_name(self) -> str:
        """Вернуть текст названия первой кампании."""
        return self.first_campaign.locator("p").first.text_content() or ""

    @allure.step("Получение данных первой кампании")
    def get_first_campaign_details(self) -> dict:
        """Вернуть словарь dt→dd из первой кампании."""
        terms = self.first_campaign.locator("dt").all_text_contents()
        values = self.first_campaign.locator("dd").all_text_contents()
        return dict(zip(terms, values))

    # ── Методы проверок ───────────────────────────────────────

    @allure.step("Проверка: страница кампаний загружена")
    def expect_loaded(self) -> None:
        """Проверить что страница кампаний рекламодателя загружена."""
        self.expect_url_contains(r".*/app/advertiser/campaigns")

    @allure.step("Проверка: навигация рекламодателя видна")
    def check_navigation_visible(self) -> None:
        """Проверить видимость навигации."""
        expect(self.nav_market).to_be_visible()
        expect(self.nav_campaigns).to_be_visible()
        expect(self.nav_products).to_be_visible()
        expect(self.nav_integrations).to_be_visible()
        expect(self.nav_statistics).to_be_visible()
        expect(self.nav_faq).to_be_visible()

    @allure.step("Проверка: заголовок и описание видны")
    def check_heading_visible(self) -> None:
        """Проверить видимость заголовка и описания."""
        expect(self.heading).to_be_visible()
        expect(self.description).to_be_visible()

    @allure.step("Проверка: кнопка Создать видна")
    def check_create_button_visible(self) -> None:
        """Проверить видимость кнопки создания."""
        expect(self.create_link).to_be_visible()

    @allure.step("Проверка: табы статусов видны")
    def check_tabs_visible(self) -> None:
        """Проверить видимость табов статуса кампаний."""
        expect(self.tab_active).to_be_visible()
        expect(self.tab_paused).to_be_visible()
        expect(self.tab_completed).to_be_visible()
        expect(self.tab_all).to_be_visible()

    @allure.step("Проверка: таб Активные выбран по умолчанию")
    def check_active_tab_selected(self) -> None:
        """Проверить что таб Активные выбран по умолчанию."""
        expect(self.tab_active).to_be_checked()

    @allure.step("Проверка: фильтр ведения виден")
    def check_management_filter_visible(self) -> None:
        """Проверить видимость фильтра ведения."""
        expect(self.filter_management).to_be_visible()

    @allure.step("Проверка: сортировка видна")
    def check_sort_visible(self) -> None:
        """Проверить видимость кнопки сортировки."""
        expect(self.sort_button).to_be_visible()

    @allure.step("Проверка: карусель баннеров видна")
    def check_carousel_visible(self) -> None:
        """Проверить видимость карусели."""
        expect(self.carousel_prev).to_be_visible()
        expect(self.carousel_next).to_be_visible()

    @allure.step("Проверка: первая кампания отображается")
    def check_first_campaign_visible(self) -> None:
        """Проверить что первая кампания в списке видна."""
        expect(self.first_campaign).to_be_visible()
        expect(self.first_campaign_image).to_be_visible()

    @allure.step("Проверка: список кампаний не пуст")
    def check_campaigns_list_not_empty(self) -> None:
        """Проверить что в списке есть хотя бы одна кампания."""
        count = self.campaign_items.count()
        assert count > 0, f"Список кампаний пуст (count={count})"

    @allure.step("Проверка: у первой кампании есть бейдж статуса")
    def check_first_campaign_has_status(self) -> None:
        """Проверить наличие бейджа статуса Активна."""
        expect(self.first_campaign_status_badge).to_be_visible()

    @allure.step("Проверка: у первой кампании есть бейдж ведения")
    def check_first_campaign_has_management(self) -> None:
        """Проверить наличие бейджа На ведении."""
        expect(self.first_campaign_management_badge).to_be_visible()

    @allure.step("Проверка: у первой кампании есть метрики (Отклики, Интеграции, Стоимость)")
    def check_first_campaign_has_metrics(self) -> None:
        """Проверить наличие dt-полей метрик."""
        expect(self.first_campaign_offers).to_be_visible()
        expect(self.first_campaign_integrations).to_be_visible()
        expect(self.first_campaign_cost).to_be_visible()
        expect(self.first_campaign_reward).to_be_visible()

    @allure.step("Проверка: кнопка Как это работает? видна")
    def check_how_it_works_visible(self) -> None:
        """Проверить видимость кнопки Как это работает?"""
        expect(self.how_it_works_button).to_be_visible()

    @allure.step("Проверка: футер виден")
    def check_footer_visible(self) -> None:
        """Проверить видимость футера."""
        expect(self.footer_copyright).to_be_visible()
        expect(self.footer_about_link).to_be_visible()
