"""products-06: Вернуть услугу из архива по названию из файла."""

from pathlib import Path

import allure
import pytest

from tests.pages.products_page import ProductsPage

LAST_SERVICE_NAME_PATH = Path(__file__).resolve().parents[2] / "test_data" / "last_service_name.txt"


@pytest.mark.regression
@pytest.mark.products
@allure.epic("Продукты рекламодателя")
@allure.feature("Архив продуктов")
@allure.story("Возврат продукта из архива")
@allure.tag("Regression", "Products", "Positive")
class TestProducts06:
    """products-06: Открыть архив, найти по имени из файла, разархивировать."""

    @allure.title("products-06: Вернуть из архива услугу по target_title")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_products_06_restore_from_archive(self, products_page: ProductsPage):
        # 1) Старт на странице /products
        products_page.expect_loaded()
        products_page.accept_cookies()

        # 2) Взять target_title из файла
        assert LAST_SERVICE_NAME_PATH.exists(), (
            f"Не найден файл с названием услуги: {LAST_SERVICE_NAME_PATH}. "
            "Сначала запусти тест создания/архивации услуги"
        )
        target_title = LAST_SERVICE_NAME_PATH.read_text(encoding="utf-8").strip()
        assert target_title, "Файл last_service_name.txt пуст"

        # 3) Нажать «Архив продуктов»
        products_page.click_archive()
        products_page.expect_archive_loaded()

        # 4) Скролл-цикл и поиск карточки по точному названию
        found_index = products_page.find_service_index_by_title_while(target_title)
        found_title = products_page.get_service_title_by_index(found_index)
        assert found_title == target_title, (
            f"Заголовок карточки не равен target_title: '{found_title}' != '{target_title}'"
        )

        # 5) Разархивировать найденный продукт
        products_page.unarchive_service_by_index(found_index)

        allure.attach(
            f"Разархивирован продукт: {found_title}\nИндекс: {found_index}",
            name="Restore from archive result",
            attachment_type=allure.attachment_type.TEXT,
        )
