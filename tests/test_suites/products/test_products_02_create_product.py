"""products-02: Успешное создание продукта с рандомными данными."""
import allure
import pytest
from playwright.sync_api import Page, expect

from tests.pages.create_product_page import CreateProductPage
from tests.pages.products_page import ProductsPage
from tests.test_data.product_generator import generate_product_data


@pytest.mark.regression
@pytest.mark.products
@allure.epic("Продукты рекламодателя")
@allure.feature("Создание продукта")
@allure.story("Успешное создание")
@allure.tag("Regression", "Products", "Positive")
class TestProducts02:
    """products-02: Создание продукта с заполнением всех полей."""

    @allure.title("products-02: Заполнение всех полей (рандом) → продукт создан")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description(
        "Шаги:\n"
        "1) Открыть страницу создания продукта\n"
        "2) Загрузить изображение\n"
        "3) Заполнить все поля рандомными реалистичными данными\n"
        '4) Нажать "Создать"\n\n'
        "Ожидаемый результат:\n"
        "1) Пользователь переходит на /app/advertiser/products\n"
        "2) Созданный продукт отображается в списке"
    )
    def test_products_02_create_product(
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

        # ОР 1) Переход на страницу списка продуктов
        products_page = ProductsPage(page)
        products_page.expect_loaded()

        # ОР 2) Созданный продукт отображается в списке
        product_name = page.get_by_text(data.name).first
        expect(product_name).to_be_visible(timeout=10000)
