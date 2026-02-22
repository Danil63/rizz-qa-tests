"""products-04: Навигация с /products на /campaigns по кнопке в навбаре.

Сценарий:
    1) Открыть /app/advertiser/products
    2) Нажать «Кампании» в навигационной панели
    3) Проверить переход на /app/advertiser/campaigns
    4) Проверить что заголовок «Кампании» виден
"""
import allure
import pytest
from playwright.sync_api import Page

from tests.pages.products_page import ProductsPage
from tests.pages.campaigns_page import CampaignsPage


@pytest.mark.regression
@pytest.mark.products
@allure.epic("Продукты рекламодателя")
@allure.feature("Навигация")
@allure.story("Переход с Продуктов на Кампании через навбар")
@allure.tag("Regression", "Products", "Navigation")
class TestProducts04:
    """products-04: Навигация /products → /campaigns по навбару."""

    @allure.title(
        "products-04: Продукты → клик «Кампании» в навбаре → страница кампаний"
    )
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description(
        "Шаги:\n"
        "1) Открыть страницу /app/advertiser/products\n"
        '2) Нажать ссылку «Кампании» в навигационной панели\n'
        "3) Проверить URL /app/advertiser/campaigns\n"
        '4) Проверить заголовок «Кампании» виден'
    )
    def test_products_04_navigate_to_campaigns(
        self,
        _load_auth,
        page: Page,
    ):
        # 1) Открыть страницу продуктов
        products_page = ProductsPage(page)
        products_page.visit()
        products_page.expect_loaded()
        products_page.accept_cookies()

        # 2) Нажать «Кампании» в навигационной панели
        page.get_by_role("navigation").get_by_role("link", name="Кампании").click()

        # 3-4) Проверить переход на страницу кампаний
        campaigns_page = CampaignsPage(page)
        campaigns_page.expect_loaded()
        campaigns_page.check_heading_visible()
