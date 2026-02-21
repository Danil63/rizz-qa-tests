"""Фикстура создания рекламной кампании.

Зависимости:
  - advertiser_page (корневой conftest.py) — авторизация рекламодателя
  - created_product (product_fixture.py) — продукт уже создан

Цепочка: advertiser_page → created_product → created_campaign
"""
import allure
import pytest
from playwright.sync_api import Page

from tests.pages.campaigns_page import CampaignsPage
from tests.pages.create_campaign_page import CreateCampaignPage
from tests.test_data.campaign_generator import generate_campaign_data, CampaignData
from tests.test_data.product_generator import ProductData


@pytest.fixture()
@allure.title("Создание тестовой кампании через UI")
def created_campaign(advertiser_page: Page, created_product: ProductData) -> CampaignData:
    """Создать кампанию через UI и вернуть её данные.

    Зависит от:
      - advertiser_page — рекламодатель авторизован
      - created_product — продукт создан (используем его имя для поиска)

    Цепочка фикстур поднимается автоматически:
      auth → product → campaign
    """
    campaign_data = generate_campaign_data(
        product_name=created_product.name,
        product_price=int(created_product.price),
    )

    create_page = CreateCampaignPage(advertiser_page)
    create_page.visit()
    create_page.expect_loaded()
    create_page.accept_cookies()

    create_page.fill_all_fields(
        name=campaign_data.name,
        product_search=campaign_data.product_search,
        utm_link=campaign_data.utm_link,
        thematic=campaign_data.thematic,
        task=campaign_data.task,
        max_compensation=campaign_data.max_compensation,
    )

    create_page.click_create_campaign()

    # Ждём редирект на страницу списка кампаний
    campaigns_page = CampaignsPage(advertiser_page)
    campaigns_page.expect_loaded()

    yield campaign_data

    # Teardown: здесь можно добавить удаление кампании через UI/API
