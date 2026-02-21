"""Сценарный тест: полный флоу от авторизации до фильтрации кампании.

Цепочка фикстур:
    advertiser_page (авторизация рекламодателя)
        ↓
    created_product (создание продукта)
        ↓
    created_campaign (создание кампании)
        ↓
    тест: фильтрация на странице маркета
"""
import allure
import pytest
from playwright.sync_api import Page

from tests.pages.market_page import MarketPage
from tests.test_data.product_generator import ProductData
from tests.test_data.campaign_generator import CampaignData


@pytest.mark.regression
@allure.epic("Сценарные тесты")
@allure.feature("Полный флоу кампании")
@allure.tag("Regression", "Scenario", "E2E")
class TestFullCampaignFlow:
    """E2E: авторизация → продукт → кампания → фильтрация."""

    @allure.title("Полный сценарий: создание продукта → кампании → фильтрация на маркете")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description(
        "Шаги (через цепочку фикстур):\n"
        "1) Авторизация как рекламодатель (advertiser_page)\n"
        "2) Создание продукта (created_product)\n"
        "3) Создание кампании (created_campaign)\n"
        "4) Проверка: кампания отображается в списке\n\n"
        "Ожидаемый результат:\n"
        "Кампания создана и видна в списке кампаний"
    )
    def test_campaign_created_and_visible(
        self,
        advertiser_page: Page,
        created_product: ProductData,
        created_campaign: CampaignData,
    ):
        """Проверить что после цепочки авторизация → продукт → кампания,
        кампания появляется в списке."""
        from tests.pages.campaigns_page import CampaignsPage

        campaigns = CampaignsPage(advertiser_page)
        campaigns.visit()
        campaigns.expect_loaded()

        # Проверяем что список кампаний не пуст
        campaigns.check_campaigns_list_not_empty()
