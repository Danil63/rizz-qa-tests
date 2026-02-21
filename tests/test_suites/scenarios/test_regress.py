"""Регрессионный сценарий: все тест-кейсы по сьютам.

Порядок:
    1. Авторизация (class setup)
    2. Все тесты продуктов → teardown: продукт остаётся для кампании
    3. Все тесты кампаний → teardown: кампания остаётся для фильтрации
    4. Все тесты фильтрации → teardown: очистка

Каждый класс = отдельный сьют со своим setup/teardown.
Запуск: pytest tests/test_suites/scenarios/test_regress.py -v -s
"""
import time

import allure
import pytest
from playwright.sync_api import Page, expect

from tests.flows.auth_flow import AuthFlow
from tests.pages.products_page import ProductsPage
from tests.pages.create_product_page import CreateProductPage
from tests.pages.campaigns_page import CampaignsPage
from tests.pages.create_campaign_page import CreateCampaignPage
from tests.pages.market_page import MarketPage
from tests.components.market_components.filter_component import FilterComponent
from tests.test_data.product_generator import generate_product_data
from tests.test_data.campaign_generator import generate_campaign_data


# ══════════════════════════════════════════════════════════════
# 1. ПРОДУКТЫ
# ══════════════════════════════════════════════════════════════

@pytest.mark.regression
@allure.epic("Регресс")
@allure.feature("Продукты")
class TestRegressProducts:
    """Сьют продуктов: setup (auth + открытие страницы) → тесты → teardown."""

    @pytest.fixture(autouse=True, scope="class")
    def _setup(self, class_page: Page):
        """Setup: авторизация + данные продукта."""
        # Auth
        auth = AuthFlow(class_page)
        auth.login_with_phone("9087814701", "89087814701")
        CampaignsPage(class_page).expect_loaded()
        cookie_btn = class_page.get_by_role("button", name="Принять cookie")
        if cookie_btn.is_visible(timeout=3000):
            cookie_btn.click()

        # Сохраняем page и данные в класс
        TestRegressProducts._page = class_page
        TestRegressProducts._product_data = generate_product_data()

        yield

        # Teardown после всех тестов продуктов
        with allure.step("Teardown: очистка после сьюта продуктов"):
            # TODO: удаление продукта через API
            pass

    @allure.title("products-01: Пустая форма → ошибки валидации")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_01_create_empty(self):
        page = self._page
        create_page = CreateProductPage(page)
        create_page.visit()
        create_page.expect_loaded()
        create_page.accept_cookies()

        create_page.click_submit()

        create_page.check_all_validation_errors_visible()
        create_page.check_error_article()
        create_page.check_error_name()
        create_page.check_error_description()
        create_page.check_error_category()
        create_page.check_error_brand()
        create_page.check_error_marketplace()
        create_page.check_error_price()
        create_page.check_error_product_link()

    @allure.title("products-02: Создание продукта (рандом) → успех")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_02_create_product(self):
        page = self._page
        data = self._product_data

        allure.attach(
            f"Название: {data.name}\nАртикул: {data.article}\n"
            f"Категория: {data.category}\nБренд: {data.brand}\n"
            f"Маркетплейс: {data.marketplace}\nЦена: {data.price} ₽",
            name="Данные продукта",
            attachment_type=allure.attachment_type.TEXT,
        )

        create_page = CreateProductPage(page)
        create_page.visit()
        create_page.expect_loaded()
        create_page.accept_cookies()

        create_page.fill_all_fields(
            article=data.article,
            name=data.name,
            description=data.description,
            category=data.category,
            brand=data.brand,
            marketplace=data.marketplace,
            price=data.price,
            product_link=data.product_link,
            task_type=data.task_type,
        )
        create_page.click_submit()

        products_page = ProductsPage(page)
        products_page.expect_loaded()

    @allure.title("products-03: Навигация Продукты → Кампании")
    @allure.severity(allure.severity_level.NORMAL)
    def test_03_navigate_to_campaigns(self):
        page = self._page

        products_page = ProductsPage(page)
        products_page.visit()
        products_page.expect_loaded()
        products_page.accept_cookies()

        page.get_by_role("navigation").get_by_role("link", name="Кампании").click()

        campaigns_page = CampaignsPage(page)
        campaigns_page.expect_loaded()
        campaigns_page.check_heading_visible()


# ══════════════════════════════════════════════════════════════
# 2. КАМПАНИИ
# ══════════════════════════════════════════════════════════════

@pytest.mark.regression
@allure.epic("Регресс")
@allure.feature("Кампании")
class TestRegressCampaigns:
    """Сьют кампаний: setup (auth + открытие) → тесты → teardown."""

    @pytest.fixture(autouse=True, scope="class")
    def _setup(self, class_page: Page):
        """Setup: авторизация."""
        auth = AuthFlow(class_page)
        auth.login_with_phone("9087814701", "89087814701")
        CampaignsPage(class_page).expect_loaded()
        cookie_btn = class_page.get_by_role("button", name="Принять cookie")
        if cookie_btn.is_visible(timeout=3000):
            cookie_btn.click()

        TestRegressCampaigns._page = class_page

        yield

        with allure.step("Teardown: очистка после сьюта кампаний"):
            # TODO: удаление кампании через API
            pass

    @allure.title("campaigns-01: Пустая форма → 5 ошибок валидации")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_01_create_empty(self):
        page = self._page

        campaigns_page = CampaignsPage(page)
        campaigns_page.visit()
        campaigns_page.expect_loaded()
        campaigns_page.accept_cookies()
        campaigns_page.click_create()

        create_page = CreateCampaignPage(page)
        create_page.expect_loaded()
        create_page.accept_cookies()

        create_page.click_create_campaign()
        page.wait_for_timeout(1000)

        create_page.check_still_on_create_page()
        create_page.check_all_validation_errors_visible()
        create_page.check_error_name()
        create_page.check_error_product()
        create_page.check_error_content_format()
        create_page.check_error_thematic()
        create_page.check_error_task()

    @allure.title("campaigns-02: Создание кампании (рандом) → успех")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_02_create(self):
        page = self._page

        data = generate_campaign_data(product_name="Гвозди", product_price=75)

        allure.attach(
            f"Название: {data.name}\nПредмет рекламы: {data.product_search}\n"
            f"UTM: {data.utm_link}\nТематика: {data.thematic}\n"
            f"Компенсация: {data.max_compensation} ₽",
            name="Данные кампании",
            attachment_type=allure.attachment_type.TEXT,
        )

        campaigns_page = CampaignsPage(page)
        campaigns_page.visit()
        campaigns_page.expect_loaded()
        campaigns_page.accept_cookies()
        campaigns_page.click_create()

        create_page = CreateCampaignPage(page)
        create_page.expect_loaded()
        create_page.accept_cookies()

        create_page.fill_all_fields(
            name=data.name,
            product_search=data.product_search,
            utm_link=data.utm_link,
            thematic=data.thematic,
            task=data.task,
            max_compensation=data.max_compensation,
        )
        create_page.click_create_campaign()

        result_page = CampaignsPage(page)
        result_page.expect_loaded()
        time.sleep(3)

    @allure.title("campaigns-03: Фильтр «Самостоятельно» → список виден")
    @allure.severity(allure.severity_level.NORMAL)
    def test_03_filter_self_managed(self):
        page = self._page

        campaigns_page = CampaignsPage(page)
        campaigns_page.visit()
        campaigns_page.expect_loaded()
        campaigns_page.accept_cookies()

        campaigns_page.check_active_tab_selected()
        campaigns_page.select_management_filter("Самостоятельно")
        page.wait_for_timeout(1500)

        campaigns_page.check_active_tab_selected()
        expect(campaigns_page.filter_management).to_contain_text("Самостоятельно")


# ══════════════════════════════════════════════════════════════
# 3. ФИЛЬТРАЦИЯ НА МАРКЕТЕ
# ══════════════════════════════════════════════════════════════

@pytest.mark.regression
@allure.epic("Регресс")
@allure.feature("Фильтрация на маркете")
class TestRegressFilters:
    """Сьют фильтрации: setup (auth блогера + маркет) → тесты → teardown."""

    @pytest.fixture(autouse=True, scope="class")
    def _setup(self, class_page: Page):
        """Setup: авторизация как блогер."""
        import json
        from pathlib import Path

        state_path = Path(__file__).parent.parent / "filters" / ".." / ".." / "stage" / "blogger_state.json"
        state_path = state_path.resolve()

        if state_path.exists():
            state = json.loads(state_path.read_text())
            for cookie in state.get("cookies", []):
                class_page.context.add_cookies([cookie])

        market = MarketPage(class_page)
        market.visit()
        market.expect_loaded()
        market.accept_cookies()

        TestRegressFilters._page = class_page

        yield

        with allure.step("Teardown: очистка после сьюта фильтрации"):
            # Финальная очистка всего регресса
            pass

    @allure.title("filters-01: Поиск по текстовому вводу")
    @allure.severity(allure.severity_level.NORMAL)
    def test_01_search_input(self):
        filters = FilterComponent(self._page)
        filters.fill_search("тест")
        filters.check_cards_visible()

    @allure.title("filters-02: Очистка поиска")
    @allure.severity(allure.severity_level.NORMAL)
    def test_02_clear_search(self):
        filters = FilterComponent(self._page)
        filters.fill_search("тест")
        filters.clear_search()
        filters.check_cards_visible()

    @allure.title("filters-04: Фильтр по маркетплейсу")
    @allure.severity(allure.severity_level.NORMAL)
    def test_04_marketplace(self):
        filters = FilterComponent(self._page)
        filters.select_dropdown_option("Маркетплейс", "ВсеИнструменты")
        filters.check_cards_visible()

    @allure.title("filters-05: Фильтр по соцсети")
    @allure.severity(allure.severity_level.NORMAL)
    def test_05_social_network(self):
        filters = FilterComponent(self._page)
        filters.select_dropdown_option("Социальная сеть", "Instagram")
        filters.check_cards_visible()

    @allure.title("filters-06: Фильтр по категории")
    @allure.severity(allure.severity_level.NORMAL)
    def test_06_category(self):
        filters = FilterComponent(self._page)
        filters.select_dropdown_option("Категория", "Строительство и ремонт")
        filters.check_cards_visible()

    @allure.title("filters-07: Фильтр по вознаграждению")
    @allure.severity(allure.severity_level.NORMAL)
    def test_07_reward(self):
        filters = FilterComponent(self._page)
        filters.select_dropdown_option("Вознаграждение", "Бартер")
        filters.check_cards_visible()
