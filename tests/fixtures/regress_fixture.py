"""Фикстура полного регрессионного сценария.

scope="class" — один setup на весь тестовый класс:
    1. Авторизация (advertiser_page, переопределён как class-scoped в scenarios/conftest.py)
    2. Создание продукта
    3. Создание кампании
    4. yield → все тесты класса работают с этими данными
    5. Teardown: очистка один раз после всех тестов
"""
import allure
import pytest
from dataclasses import dataclass
from playwright.sync_api import Page

from tests.pages.products_page import ProductsPage
from tests.pages.create_product_page import CreateProductPage
from tests.pages.campaigns_page import CampaignsPage
from tests.pages.create_campaign_page import CreateCampaignPage
from tests.test_data.product_generator import generate_product_data, ProductData
from tests.test_data.campaign_generator import generate_campaign_data, CampaignData


@dataclass
class RegressData:
    """Данные регрессионного прогона."""
    product: ProductData
    campaign: CampaignData
    page: Page


@pytest.fixture(scope="class")
@allure.title("Регресс: setup auth → product → campaign")
def regress(advertiser_page: Page) -> RegressData:
    """Полный регрессионный сценарий.

    Зависимости:
        - advertiser_page (class-scoped, из scenarios/conftest.py)

    Setup (один раз на класс):
        1. Авторизация — через advertiser_page
        2. Создание продукта через UI
        3. Создание кампании через UI

    Yield:
        RegressData с product, campaign, page

    Teardown (один раз после всех тестов класса):
        Очистка созданных сущностей
    """
    page = advertiser_page

    # ── 1. Создание продукта ──────────────────────────────────

    with allure.step("Создание тестового продукта"):
        product_data = generate_product_data()

        create_product = CreateProductPage(page)
        create_product.visit()
        create_product.expect_loaded()
        create_product.accept_cookies()

        create_product.fill_all_fields(
            article=product_data.article,
            name=product_data.name,
            description=product_data.description,
            category=product_data.category,
            brand=product_data.brand,
            marketplace=product_data.marketplace,
            price=product_data.price,
            product_link=product_data.product_link,
            task_type=product_data.task_type,
        )
        create_product.click_submit()

        products_page = ProductsPage(page)
        products_page.expect_loaded()

    # ── 2. Создание кампании ──────────────────────────────────

    with allure.step("Создание тестовой кампании"):
        campaign_data = generate_campaign_data(
            product_name=product_data.name,
            product_price=int(product_data.price),
        )

        create_campaign = CreateCampaignPage(page)
        create_campaign.visit()
        create_campaign.expect_loaded()
        create_campaign.accept_cookies()

        create_campaign.fill_all_fields(
            name=campaign_data.name,
            product_search=campaign_data.product_search,
            utm_link=campaign_data.utm_link,
            thematic=campaign_data.thematic,
            task=campaign_data.task,
            max_compensation=campaign_data.max_compensation,
        )
        create_campaign.click_create_campaign()

        campaigns_page = CampaignsPage(page)
        campaigns_page.expect_loaded()

    # ── 3. Yield данные ───────────────────────────────────────

    result = RegressData(
        product=product_data,
        campaign=campaign_data,
        page=page,
    )

    yield result

    # ── 4. Teardown: очистка (один раз) ───────────────────────

    with allure.step("Teardown: очистка тестовых данных"):
        # TODO: удаление через API когда эндпоинты будут готовы
        pass
