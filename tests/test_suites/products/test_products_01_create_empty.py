"""products-01: Создание продукта с пустыми полями (негативный)."""

import pytest

from tests.pages.create_product_page import CreateProductPage


@pytest.mark.regression
@pytest.mark.products
class TestProducts01:
    """products-01: Отправка пустой формы создания продукта."""

    def test_products_01_create_empty(self, create_product_page: CreateProductPage):
        # 1) Страница уже открыта через фикстуру

        # 2) Нажать "Создать" без заполнения
        create_product_page.click_submit()

        # ОР: Проверяем каждую ошибку
        create_product_page.check_all_validation_errors_visible()
        create_product_page.check_error_article()
        create_product_page.check_error_name()
        create_product_page.check_error_description()
        create_product_page.check_error_category()
        create_product_page.check_error_brand()
        create_product_page.check_error_marketplace()
        create_product_page.check_error_price()
        create_product_page.check_error_product_link()
