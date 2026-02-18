"""products-02: Успешное создание продукта."""
import allure
import pytest
from playwright.sync_api import Page, expect

from tests.pages.create_product_page import CreateProductPage
from tests.pages.products_page import ProductsPage


# ── Тестовые данные ───────────────────────────────────────────

PRODUCT_DATA = {
    "article": "TEST-AUTO-12345",
    "name": "Гвозди для монтажного пистолета FEDAST 14мм",
    "description": "Гвозди кованые для монтажного пистолета HILTI BX3, размер 14 мм, 1000 шт.",
    "category": "Строительство и ремонт",
    "brand": "FEDAST",
    "marketplace": "ВсеИнструменты",
    "price": "950",
    "product_link": "https://www.vseinstrumenti.ru/product/gvozdi-fedast-14mm",
    "task_type": "Товар",
}


@pytest.mark.regression
@pytest.mark.products
@allure.epic("Продукты рекламодателя")
@allure.feature("Создание продукта")
@allure.story("Успешное создание")
@allure.tag("Regression", "Products", "Positive")
class TestProducts02:
    """products-02: Создание продукта с заполнением всех полей."""

    @allure.title("products-02: Заполнение всех полей → продукт создан")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description(
        "Шаги:\n"
        "1) Открыть страницу создания продукта\n"
        "2) Загрузить изображение\n"
        "3) Выбрать тип задания — Товар\n"
        "4) Заполнить Артикул: TEST-AUTO-12345\n"
        "5) Заполнить Название: Гвозди для монтажного пистолета FEDAST 14мм\n"
        "6) Заполнить Описание\n"
        "7) Выбрать Категорию: Строительство и ремонт\n"
        "8) Заполнить Бренд: FEDAST\n"
        "9) Выбрать Маркетплейс: ВсеИнструменты\n"
        "10) Заполнить Цену: 950\n"
        "11) Заполнить Ссылку на товар\n"
        '12) Нажать "Создать"\n\n'
        "Ожидаемый результат:\n"
        "1) Пользователь переходит на /app/advertiser/products\n"
        "2) Созданный продукт отображается в списке"
    )
    def test_products_02_create_product(
        self,
        create_product_page: CreateProductPage,
        page: Page,
    ):
        # 1) Страница уже открыта через фикстуру

        # 2-11) Заполнить все поля
        create_product_page.fill_all_fields(**PRODUCT_DATA)

        # 12) Нажать "Создать"
        create_product_page.click_submit()

        # ОР 1) Переход на страницу списка продуктов
        products_page = ProductsPage(page)
        products_page.expect_loaded()

        # ОР 2) Созданный продукт отображается в списке
        product_name = page.get_by_text(PRODUCT_DATA["name"]).first
        expect(product_name).to_be_visible(timeout=10000)
