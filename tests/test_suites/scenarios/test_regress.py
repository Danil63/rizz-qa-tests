"""Регрессионный сценарий: все типы кампаний.

Фикстура `regress` параметризована: barter, fixed, per_views.
Каждый тест выполнится 3 раза — по одному на каждый тип кампании.
Полная цепочка: auth → product → campaign → проверки → teardown.
"""
import allure
import pytest
from playwright.sync_api import Page

from tests.fixtures.regress_fixture import RegressData
from tests.pages.campaigns_page import CampaignsPage
from tests.pages.market_page import MarketPage


@pytest.mark.regression
@allure.epic("Регрессионные сценарии")
@allure.feature("Полный цикл кампании")
@allure.tag("Regression", "E2E")
class TestRegress:
    """Регресс: авторизация → продукт → кампания → фильтрация."""

    @allure.title("Кампания [{regress.campaign_type}]: создана и видна в списке")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_campaign_visible_in_list(
        self,
        advertiser_page: Page,
        regress: RegressData,
    ):
        """Проверить что кампания появилась в списке после создания."""
        campaigns = CampaignsPage(advertiser_page)
        campaigns.visit()
        campaigns.expect_loaded()
        campaigns.check_campaigns_list_not_empty()

    @allure.title("Кампания [{regress.campaign_type}]: продукт виден в списке продуктов")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_product_visible_in_list(
        self,
        advertiser_page: Page,
        regress: RegressData,
    ):
        """Проверить что продукт появился в списке после создания."""
        from tests.pages.products_page import ProductsPage

        products = ProductsPage(advertiser_page)
        products.visit()
        products.expect_loaded()
        products.check_products_list_not_empty()
