"""POM: Страница списка продуктов рекламодателя."""
import allure
from playwright.sync_api import Page, expect

from tests.pages.base_page import BasePage


class ProductsPage(BasePage):
    """Page Object для https://app.rizz.market/app/advertiser/products."""

    URL = "https://app.rizz.market/app/advertiser/products"

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
        self.user_avatar_button = page.get_by_role("button", name="user avatar")

        # ── Уведомление Telegram ──────────────────────────────
        self.telegram_notification = page.get_by_text(
            "Подключите уведомления в Telegram"
        )

        # ── Заголовок и описание ──────────────────────────────
        self.heading = page.get_by_role("heading", name="Список продуктов")
        self.description = page.get_by_text("Список добавленных вручную продуктов и по API.")
        self.how_it_works_button = page.get_by_role("button", name="Как это работает?")

        # ── Кнопки действий ───────────────────────────────────
        self.create_link = page.get_by_role("link", name="Создать")
        self.sync_api_link = page.get_by_role("link", name="Синхронизация по API")
        self.archive_link = page.get_by_role("link", name="Архив продуктов")

        # ── Фильтр Товар/Услуга ──────────────────────────────
        self.filter_type_button = page.get_by_role("button", name="Товар")
        self.filter_service_button = page.get_by_role("button", name="Услуга")

        # ── Список продуктов/услуг ───────────────────────────
        self.product_items = page.get_by_role("listitem")
        self.service_cards = page.locator("li:has(a[href*='/app/advertiser/products/']):has(button)")
        self.product_titles = page.locator("li a img[alt]")
        self.first_product = page.get_by_role("listitem").first
        self.first_product_link = self.first_product.get_by_role("link")
        self.first_product_image = self.first_product.locator("img").first
        self.first_product_menu_button = self.first_product.get_by_role("button")

        # ── Пагинация ────────────────────────────────────────
        self.load_more = page.get_by_role("heading", name="Загрузить ещё")

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

    @allure.step('Выбор типа продукта: "{option}"')
    def select_product_type(self, option: str) -> None:
        """Открыть dropdown Товар/Услуга и выбрать опцию."""
        if self.filter_type_button.is_visible():
            self.filter_type_button.click()
        else:
            self.filter_service_button.click()
        self.page.get_by_role("option", name=option).click()

    @allure.step("Получить количество карточек услуг")
    def get_service_cards_count(self) -> int:
        """Вернуть количество карточек в текущем списке услуг."""
        return self.service_cards.count()

    @allure.step("Получить заголовок услуги по индексу")
    def get_service_title_by_index(self, index: int) -> str:
        """Достаёт заголовок услуги из карточки (устойчиво, без img[alt])."""
        card = self.service_cards.nth(index)
        text = card.get_by_role("link").first.inner_text().strip()
        return text.splitlines()[0].strip() if text else ""

    @allure.step("Найти услугу по названию циклом while")
    def find_service_index_by_title_while(self, target_title: str) -> int:
        """Вернуть индекс услуги по названию (по тексту из переменной), используя while-цикл."""
        total = self.get_service_cards_count()
        idx = 0
        while idx < total:
            current_title = self.get_service_title_by_index(idx)
            if target_title in current_title:
                return idx
            idx += 1
        raise AssertionError(f"Услуга с названием '{target_title}' не найдена. total={total}")

    @allure.step("Архивировать услугу по индексу")
    def archive_service_by_index(self, index: int) -> None:
        """Открыть меню троеточия у карточки и нажать 'Архивировать'."""
        card = self.service_cards.nth(index)
        card.get_by_role("button").click()
        self.page.get_by_role("menuitem", name="Архивировать").click()

    @allure.step("Клик по первому продукту")
    def click_first_product(self) -> None:
        """Перейти в первый продукт из списка."""
        self.first_product_link.click()

    @allure.step("Клик по кнопке Создать")
    def click_create(self) -> None:
        """Нажать кнопку Создать."""
        self.create_link.click()

    @allure.step("Клик по кнопке Архив продуктов")
    def click_archive(self) -> None:
        """Нажать кнопку Архив продуктов."""
        self.archive_link.click()

    # ── Методы получения данных ────────────────────────────────

    @allure.step("Получение названия первого продукта")
    def get_first_product_name(self) -> str:
        """Вернуть alt-текст картинки первого продукта (название)."""
        return self.first_product_image.get_attribute("alt") or ""

    @allure.step("Получение данных первого продукта")
    def get_first_product_details(self) -> dict:
        """Вернуть словарь dt→dd из первого продукта."""
        terms = self.first_product.locator("dt").all_text_contents()
        values = self.first_product.locator("dd").all_text_contents()
        return dict(zip(terms, values))

    # ── Методы проверок ───────────────────────────────────────

    @allure.step("Проверка: страница продуктов загружена")
    def expect_loaded(self) -> None:
        """Проверить что страница продуктов рекламодателя загружена."""
        self.expect_url_contains(r".*/app/advertiser/products")
        expect(self.heading).to_be_visible()

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

    @allure.step("Проверка: кнопки действий видны")
    def check_action_buttons_visible(self) -> None:
        """Проверить видимость кнопок Создать, Синхронизация, Архив."""
        expect(self.create_link).to_be_visible()
        expect(self.sync_api_link).to_be_visible()
        expect(self.archive_link).to_be_visible()

    @allure.step("Проверка: фильтр Товар/Услуга виден")
    def check_filter_type_visible(self) -> None:
        """Проверить видимость dropdown фильтра типа."""
        expect(self.filter_type_button).to_be_visible()

    @allure.step("Проверка: первый продукт отображается")
    def check_first_product_visible(self) -> None:
        """Проверить что первый продукт в списке виден."""
        expect(self.first_product).to_be_visible()
        expect(self.first_product_image).to_be_visible()

    @allure.step("Проверка: список продуктов не пуст")
    def check_products_list_not_empty(self) -> None:
        """Проверить что в списке есть хотя бы один продукт."""
        count = self.product_items.count()
        assert count > 0, f"Список продуктов пуст (count={count})"

    @allure.step("Проверка: у первого продукта есть бейдж «На ведении»")
    def check_first_product_has_status_badge(self) -> None:
        """Проверить наличие бейджа статуса у первого продукта."""
        badge = self.first_product.locator(".rounded-full.border")
        expect(badge).to_be_visible()

    @allure.step("Проверка: у первого продукта есть кнопка меню (три точки)")
    def check_first_product_has_menu(self) -> None:
        """Проверить что у первого продукта есть кнопка меню."""
        expect(self.first_product_menu_button).to_be_visible()

    @allure.step("Проверка: ссылка Как это работает? видна")
    def check_how_it_works_visible(self) -> None:
        """Проверить видимость кнопки Как это работает?"""
        expect(self.how_it_works_button).to_be_visible()

    @allure.step("Проверка: футер виден")
    def check_footer_visible(self) -> None:
        """Проверить видимость футера."""
        expect(self.footer_copyright).to_be_visible()
        expect(self.footer_about_link).to_be_visible()
