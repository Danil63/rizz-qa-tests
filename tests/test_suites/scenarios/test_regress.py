"""Регрессионный сценарий: полный цикл.

Фикстура `regress` (scope=class):
    Setup: auth → product → campaign (один раз)
    Тесты: все проверки по порядку сверху вниз
    Teardown: очистка (один раз после всех тестов)
"""
import allure
import pytest

from tests.fixtures.regress_fixture import RegressData
from tests.pages.products_page import ProductsPage
from tests.pages.campaigns_page import CampaignsPage
from tests.pages.market_page import MarketPage


@pytest.mark.regression
@allure.epic("Регрессионные сценарии")
@allure.feature("Полный цикл: продукт → кампания → фильтрация")
@allure.tag("Regression", "E2E")
class TestRegress:
    """Полный регресс.

    Порядок тестов — сверху вниз.
    Все работают с одним набором данных (regress fixture, scope=class).
    Teardown — один раз после последнего теста.
    """

    # ── Продукт ───────────────────────────────────────────────

    @allure.title("Продукт создан и виден в списке")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_01_product_visible(self, regress: RegressData):
        """Проверить что продукт появился в списке после создания."""
        products = ProductsPage(regress.page)
        products.visit()
        products.expect_loaded()
        products.check_products_list_not_empty()

    @allure.title("Продукт: название совпадает")
    @allure.severity(allure.severity_level.NORMAL)
    def test_02_product_name(self, regress: RegressData):
        """Проверить что первый продукт имеет корректное название."""
        products = ProductsPage(regress.page)
        products.visit()
        products.expect_loaded()
        products.check_first_product_visible()

    # ── Кампания ──────────────────────────────────────────────

    @allure.title("Кампания создана и видна в списке")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_03_campaign_visible(self, regress: RegressData):
        """Проверить что кампания появилась в списке."""
        campaigns = CampaignsPage(regress.page)
        campaigns.visit()
        campaigns.expect_loaded()
        campaigns.check_campaigns_list_not_empty()

    @allure.title("Кампания: есть бейдж статуса")
    @allure.severity(allure.severity_level.NORMAL)
    def test_04_campaign_has_status(self, regress: RegressData):
        """Проверить что у кампании есть бейдж статуса."""
        campaigns = CampaignsPage(regress.page)
        campaigns.visit()
        campaigns.expect_loaded()
        campaigns.check_first_campaign_has_status()

    # ── Фильтрация на маркете ─────────────────────────────────

    @allure.title("Маркет: страница загружается")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_05_market_loads(self, regress: RegressData):
        """Проверить что страница маркета загружается."""
        market = MarketPage(regress.page)
        market.visit()
        market.expect_loaded()

    @allure.title("Маркет: кампании отображаются в выдаче")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_06_market_has_campaigns(self, regress: RegressData):
        """Проверить что на маркете есть кампании."""
        market = MarketPage(regress.page)
        market.visit()
        market.expect_loaded()
        market.check_campaigns_visible()

    # После test_06 → teardown regress → очистка
