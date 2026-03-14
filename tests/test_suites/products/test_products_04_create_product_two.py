"""products-04: Успешное создание второго продукта с рандомными данными."""

import json
from pathlib import Path

import pytest
from playwright.sync_api import Page

from tests.pages.create_product_page import CreateProductPage
from tests.pages.products_page import ProductsPage
from tests.test_data.product_generator import generate_product_data

LAST_PRODUCT_TWO_META_PATH = (
    Path(__file__).resolve().parents[2] / "test_data" / "last_product_two_meta.json"
)


@pytest.mark.regression
@pytest.mark.products
class TestProducts04:
    """products-04: Создание второго продукта с заполнением всех полей."""

    def test_products_04_create_product_two(
        self,
        create_product_page: CreateProductPage,
        page: Page,
    ):
        # Генерируем рандомные данные
        data = generate_product_data()

        # Логируем в Allure что именно сгенерировали

        # 1) Страница уже открыта через фикстуру

        # 2-3) Заполнить все поля
        create_product_page.fill_all_fields(
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

        # 4) Нажать "Создать"
        create_product_page.click_submit()

        # Важно для prod: дать бэкенду зафиксировать создание сущности
        create_product_page.page.wait_for_timeout(3000)

        # Сохраняем данные второго созданного продукта в отдельный файл
        LAST_PRODUCT_TWO_META_PATH.parent.mkdir(parents=True, exist_ok=True)
        LAST_PRODUCT_TWO_META_PATH.write_text(
            json.dumps(
                {
                    "name": data.name,
                    "marketplace": data.marketplace,
                    "category": data.category,
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        # ОР) Переход на страницу списка продуктов
        products_page = ProductsPage(page)
        products_page.expect_url_contains(r".*/app/advertiser/products", timeout=15000)
