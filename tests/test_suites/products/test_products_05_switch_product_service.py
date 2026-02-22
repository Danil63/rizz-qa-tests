"""products-05: Переход Товар -> Услуга и архивация выбранной услуги."""

import allure
import pytest
from pathlib import Path

from tests.pages.products_page import ProductsPage

LAST_SERVICE_NAME_PATH = Path(__file__).resolve().parents[2] / "test_data" / "last_service_name.txt"


@pytest.mark.regression
@pytest.mark.products
@allure.epic("Продукты рекламодателя")
@allure.feature("Фильтрация и архивация")
@allure.story("Переход Товар/Услуга и архивация через меню")
@allure.tag("Regression", "Products", "Positive")
class TestProducts05:
    """products-05: Выбрать Услуга, найти карточку while-циклом, архивировать."""

    @allure.title("products-05: Товар -> Услуга -> найти по заголовку -> Архивировать")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_products_05_switch_product_service(self, products_page: ProductsPage):
        # 1) Старт на странице продуктов
        products_page.expect_loaded()
        products_page.accept_cookies()

        # 2) Dropdown "Товар" -> выбрать "Услуга"
        products_page.select_product_type("Услуга")

        # 3) Берём target_title из предыдущего теста создания услуги
        assert LAST_SERVICE_NAME_PATH.exists(), (
            f"Не найден файл с названием услуги: {LAST_SERVICE_NAME_PATH}. "
            "Сначала запусти test_products_02_create_service.py"
        )
        target_title = LAST_SERVICE_NAME_PATH.read_text(encoding="utf-8").strip()
        assert target_title, "Файл last_service_name.txt пуст"

        # 4) Циклом while пройти заголовки и найти нужный
        found_index = products_page.find_service_index_by_title_while(target_title)
        found_title = products_page.get_service_title_by_index(found_index)
        assert found_title == target_title, (
            f"Заголовок карточки не равен target_title: '{found_title}' != '{target_title}'"
        )

        allure.attach(
            f"Target услуга: {target_title}\nНайденная услуга: {found_title}\nИндекс: {found_index}",
            name="Проверка совпадения заголовка перед архивацией",
            attachment_type=allure.attachment_type.TEXT,
        )

        # 5) Нажать троеточие и выбрать "Архивировать"
        products_page.archive_service_by_index(found_index)

        # 6) Явная пауза 3 секунды после архивации
        products_page.page.wait_for_timeout(3000)
