"""products-04: Успешное создание услуги с рандомными данными."""
import random
import string

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
class TestProducts04:
    """products-04: Создание услуги с заполнением полей."""

    @allure.title("products-04: Создать услугу (рандом) → возврат на список продуктов")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_products_04_create_service(self, products_page: ProductsPage):
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
        article = f"{''.join(random.choices(string.ascii_uppercase, k=3))}-{random.randint(10000, 99999)}"
        name = f"Мойка окон {random.randint(100, 999)}"
        brand = f"ServiceBrand{random.randint(100, 999)}"
        price = str(random.randint(50, 110))
        product_link = f"https://www.avito.ru/item/{random.randint(10000000, 99999999)}"

        allure.attach(
            f"Тип: Услуга\n"
            f"Артикул: {article}\n"
            f"Название: {name}\n"
            f"Описание: {random_desc}\n"
            f"Категория: Бытовая химия\n"
            f"Бренд: {brand}\n"
            f"Маркетплейс: Авито\n"
            f"Цена: {price} ₽\n"
            f"Ссылка: {product_link}",
            name="Сгенерированные данные услуги",
            attachment_type=allure.attachment_type.TEXT,
        )

        # 5) Заполнить форму
        create_page.upload_image()
        create_page.fill_article(article)
        create_page.fill_name(name)
        create_page.fill_description(random_desc)

        # Категория: открыть dropdown -> скролл вниз -> выбрать "Бытовая химия"
        create_page.select_category.click()
        category_option = create_page.page.get_by_role("option", name="Бытовая химия", exact=True)
        category_option.scroll_into_view_if_needed()
        category_option.click()

        create_page.fill_brand(brand)

        # Маркетплейс: выбрать Авито
        create_page.select_marketplace_option("Авито")

        create_page.fill_price(price)
        create_page.fill_product_link(product_link)

        # 6) Нажать создать
        create_page.click_submit()

        # 7) Пользователь на экране списка продуктов
        result_products_page = ProductsPage(create_page.page)
        result_products_page.expect_loaded()
