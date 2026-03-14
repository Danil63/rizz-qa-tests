"""products-04: Навигация с /products на /campaigns по кнопке в навбаре.

Сценарий:
    1) Открыть /app/advertiser/products
    2) Нажать «Кампании» в навигационной панели
    3) Проверить переход на /app/advertiser/campaigns
    4) Проверить что заголовок «Кампании» виден
"""

import pytest
from playwright.sync_api import Page

from tests.pages.campaigns_page import CampaignsPage
from tests.pages.products_page import ProductsPage


@pytest.mark.regression
@pytest.mark.products
class TestProducts04:
    """products-04: Навигация /products → /campaigns по навбару."""

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
