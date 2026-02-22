"""products-02: Успешное создание услуги с рандомными данными."""
import random

import allure
import pytest
from tests.pages.create_product_page import CreateProductPage
from tests.pages.products_page import ProductsPage
from tests.test_data.product_generator import generate_product_data


@pytest.mark.regression
@pytest.mark.products
@allure.epic("Продукты рекламодателя")
@allure.feature("Создание услуги")
@allure.story("Успешное создание")
@allure.tag("Regression", "Products", "Positive")
class TestProducts02:
    """products-02: Создание услуги с заполнением полей."""

    @allure.title("products-02: Создать услугу (рандом) → возврат на список продуктов")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_products_02_create_service(self, products_page: ProductsPage):
        # 1) Тест стартует на странице списка продуктов
        products_page.expect_loaded()

        # 2) Нажать "+Создать"
        products_page.click_create()

        # 3) Переключиться на страницу создания и выбрать тип "Услуга"
        create_page = CreateProductPage(products_page.page)
        create_page.expect_loaded()
        create_page.select_task_type("Услуга")

        # 4) Рандомные данные
        random_desc = generate_product_data().description
        name = f"Мойка окон {random.randint(100, 999)}"

        allure.attach(
            f"Тип: Услуга\n"
            f"Название: {name}\n"
            f"Описание: {random_desc}\n"
            f"Категория: Бытовая химия",
            name="Сгенерированные данные услуги",
            attachment_type=allure.attachment_type.TEXT,
        )

        # 5) Заполнить service-поля
        create_page.check_service_mode_fields_visible()
        create_page.fill_name(name)
        create_page.fill_description(random_desc)

        # Категория: открыть dropdown -> скролл вниз -> выбрать "Бытовая химия"
        create_page.select_category.click()
        category_option = create_page.page.get_by_role("option", name="Бытовая химия", exact=True)
        category_option.scroll_into_view_if_needed()
        category_option.click()

        # 6) Нажать создать
        create_page.click_submit()

        # 7) Пользователь на экране списка продуктов
        result_products_page = ProductsPage(create_page.page)
        result_products_page.expect_loaded()
