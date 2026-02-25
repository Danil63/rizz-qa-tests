"""products-03: Успешное создание продукта с рандомными данными."""
import json
from pathlib import Path

import allure
import pytest
from playwright.sync_api import Page, expect

from tests.pages.create_product_page import CreateProductPage
from tests.pages.products_page import ProductsPage
from tests.test_data.product_generator import generate_product_data

LAST_PRODUCT_NAME_PATH = Path(__file__).resolve().parents[2] / "test_data" / "last_product_name.txt"
LAST_PRODUCT_META_PATH = Path(__file__).resolve().parents[2] / "test_data" / "last_product_meta.json"


@pytest.mark.regression
@pytest.mark.products
@allure.epic("Продукты рекламодателя")
@allure.feature("Создание продукта")
@allure.story("Успешное создание")
@allure.tag("Regression", "Products", "Positive")
class TestProducts03:
    """products-03: Создание продукта с заполнением всех полей."""

    @allure.title("products-03: Заполнение всех полей (рандом) → продукт создан")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description(
        "Шаги:\n"
        "1) Открыть страницу создания продукта\n"
        "2) Загрузить изображение\n"
        "3) Заполнить все поля рандомными реалистичными данными\n"
        '4) Нажать "Создать"\n\n'
        "Ожидаемый результат:\n"
        "1) Пользователь переходит на /app/advertiser/products"
    )
    def test_products_03_create_product(
        self,
        create_product_page: CreateProductPage,
        page: Page,
    ):
        # Генерируем рандомные данные
        data = generate_product_data()

        # Логируем в Allure что именно сгенерировали
        allure.attach(
            f"Название: {data.name}\n"
            f"Артикул: {data.article}\n"
            f"Категория: {data.category}\n"
            f"Бренд: {data.brand}\n"
            f"Маркетплейс: {data.marketplace}\n"
            f"Цена: {data.price} ₽\n"
            f"Ссылка: {data.product_link}\n"
            f"Описание: {data.description}",
            name="Сгенерированные данные продукта",
            attachment_type=allure.attachment_type.TEXT,
        )

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

        # Сохраняем данные созданного продукта для использования в campaign/filters tests
        LAST_PRODUCT_NAME_PATH.parent.mkdir(parents=True, exist_ok=True)
        LAST_PRODUCT_NAME_PATH.write_text(data.name, encoding="utf-8")
        LAST_PRODUCT_META_PATH.write_text(
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
