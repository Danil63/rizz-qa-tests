"""products-01: Создание продукта с пустыми полями (негативный)."""
import allure
import pytest

from tests.pages.create_product_page import CreateProductPage


@pytest.mark.regression
@pytest.mark.products
@allure.epic("Продукты рекламодателя")
@allure.feature("Создание продукта")
@allure.story("Валидация пустой формы")
@allure.tag("Regression", "Products", "Negative")
class TestProducts01:
    """products-01: Отправка пустой формы создания продукта."""

    @allure.title("products-01: Все поля пустые → ошибки валидации")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description(
        "Шаги:\n"
        "1) Открыть страницу создания продукта\n"
        '2) Нажать кнопку "Создать" без заполнения полей\n\n'
        "Ожидаемый результат:\n"
        "1) Артикул — «Значение слишком маленькое. Минимум: 5»\n"
        "2) Название — «Обязательное поле»\n"
        "3) Описание — «Обязательное поле»\n"
        "4) Категория — «Обязательное поле»\n"
        "5) Бренд — «Обязательное поле»\n"
        "6) Маркетплейс — «Обязательное поле»\n"
        "7) Цена — «Обязательное поле»\n"
        "8) Ссылка на товар — «Неверный формат ссылки»\n"
        "9) Всего ≥9 ошибок валидации"
    )
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
