"""Фикстура создания продукта рекламодателя.

Зависимость: advertiser_page (из корневого conftest.py).
Создаёт продукт через UI, после теста — может быть расширена для teardown.
"""
import allure
import pytest
from playwright.sync_api import Page

from tests.pages.products_page import ProductsPage
from tests.pages.create_product_page import CreateProductPage
from tests.test_data.product_generator import generate_product_data, ProductData


@pytest.fixture()
@allure.title("Создание тестового продукта через UI")
def created_product(advertiser_page: Page) -> ProductData:
    """Создать продукт через UI и вернуть его данные.

    Зависит от advertiser_page — рекламодатель уже авторизован.
    Использует POM: CreateProductPage.
    """
    product_data = generate_product_data()

    create_page = CreateProductPage(advertiser_page)
    create_page.visit()
    create_page.expect_loaded()
    create_page.accept_cookies()

    create_page.fill_all_fields(
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

    create_page.click_submit()

    # Ждём редирект на страницу списка продуктов
    products_page = ProductsPage(advertiser_page)
    products_page.expect_loaded()

    yield product_data

    # Teardown: здесь можно добавить удаление продукта через UI/API
