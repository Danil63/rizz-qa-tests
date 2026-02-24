"""filters-01: Поиск товара с использованием input."""
from pathlib import Path

import allure
import pytest

from tests.components.market_components.filter_component import FilterComponent

LAST_PRODUCT_NAME_PATH = Path(__file__).resolve().parents[2] / "test_data" / "last_product_name.txt"


@pytest.mark.regression
@pytest.mark.filters
@allure.epic("Маркет блогера")
@allure.feature("Фильтрация")
@allure.story("Поиск по тексту")
@allure.tag("Regression", "Filters")
class TestFilters01:
    """filters-01: Поиск товара с использованием input."""

    @allure.title("filters-01: Поиск товара с использованием input")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description(
        "Шаги:\n"
        '1) Выбрать в input значение "Гвозди для пистолета"\n\n'
        "Ожидаемый результат:\n"
        "1) В поисковой выдаче на 1 месте отображается товар "
        "с названием релевантным запросу"
    )
    def test_filters_01_search_input(self, filters: FilterComponent):
        assert LAST_PRODUCT_NAME_PATH.exists(), (
            f"Файл с названием продукта не найден: {LAST_PRODUCT_NAME_PATH}. "
            "Сначала запусти тест создания продукта."
        )
        product_name = LAST_PRODUCT_NAME_PATH.read_text(encoding="utf-8").strip()
        assert product_name, "Файл last_product_name.txt пустой"

        # 1) Ввести в поле поиска название продукта из файла
        filters.fill_search(product_name)
        filters.press_search_enter()

        # ОР: Первая карточка содержит релевантный текст
        # Берём первое слово из названия для проверки релевантности
        search_keyword = product_name.split()[0]
        filters.check_first_card_contains(search_keyword)
