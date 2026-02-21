"""Фикстура полного регрессионного сценария.

Параметризация по типу кампании: barter, fixed, per_views.
Каждый параметр прогоняет полную цепочку:
    авторизация → продукт → кампания → данные для фильтрации

Teardown: удаляет созданную кампанию и продукт.
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
    """Результат регрессионного прогона."""
    campaign_type: str
    product: ProductData
    campaign: CampaignData


@pytest.fixture(params=["barter", "fixed", "per_views"])
@allure.title("Регресс: полная цепочка auth → product → campaign")
def regress(request, advertiser_page: Page) -> RegressData:
    """Полный регрессионный сценарий.

    Параметры:
        - barter: кампания с типом оплаты Бартер
        - fixed: кампания с типом оплаты Фиксированная
        - per_views: кампания с типом оплаты За просмотры

    Цепочка:
        1. advertiser_page — авторизация (из корневого conftest.py)
        2. Создание продукта через UI
        3. Создание кампании выбранного типа через UI
        4. yield RegressData
        5. Teardown: удаление кампании и продукта
    """
    campaign_type = request.param
    page = advertiser_page

    # ── 1. Создание продукта ──────────────────────────────────

    with allure.step(f"Создание тестового продукта [{campaign_type}]"):
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

    with allure.step(f"Создание кампании типа: {campaign_type}"):
        campaign_data = generate_campaign_data(
            product_name=product_data.name,
            product_price=int(product_data.price),
        )

        create_campaign = CreateCampaignPage(page)
        create_campaign.visit()
        create_campaign.expect_loaded()
        create_campaign.accept_cookies()

        # Заполняем общие поля
        create_campaign.fill_name(campaign_data.name)
        create_campaign.select_product_by_search(campaign_data.product_search)
        create_campaign.fill_utm_link(campaign_data.utm_link)
        create_campaign.select_ig_all_formats()
        create_campaign.select_thematic(campaign_data.thematic)
        create_campaign.fill_task(campaign_data.task)

        # Выбираем тип оплаты
        if campaign_type == "barter":
            create_campaign.tab_barter.click()
            create_campaign.fill_max_compensation(campaign_data.max_compensation)
        elif campaign_type == "fixed":
            create_campaign.tab_fixed.click()
        elif campaign_type == "per_views":
            create_campaign.tab_per_views.click()

        create_campaign.toggle_auto_approve_off()
        create_campaign.click_create_campaign()

        campaigns_page = CampaignsPage(page)
        campaigns_page.expect_loaded()

    # ── 3. Yield данные для тестов ────────────────────────────

    result = RegressData(
        campaign_type=campaign_type,
        product=product_data,
        campaign=campaign_data,
    )

    yield result

    # ── 4. Teardown: удаляем кампанию и продукт ──────────────

    with allure.step(f"Teardown: очистка [{campaign_type}]"):
        # TODO: добавить удаление через API когда эндпоинты будут готовы
        # Пока — через UI или оставляем (зависит от наличия кнопки удаления)
        pass
