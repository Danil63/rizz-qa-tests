"""filters-01: Поиск по input (с актуальными данными из test_data)."""
from pathlib import Path

import allure
import pytest

from tests.components.market_components.filter_component import FilterComponent

TEST_DATA_DIR = Path(__file__).resolve().parents[2] / "test_data"
LAST_PRODUCT_NAME_PATH = TEST_DATA_DIR / "last_product_name.txt"


@pytest.mark.regression
@pytest.mark.filters
@allure.epic("Маркет блогера")
@allure.feature("Фильтрация")
@allure.story("Поиск по тексту")
@allure.tag("Regression", "Filters")
class TestFilters01:
    """filters-01: Поиск товара с использованием input."""

    @allure.title("filters-01: Поиск товара → проверка заголовков → очистка → повторный Enter")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description(
        "Шаги:\n"
        "1) Ввести в input название продукта из last_product_name.txt\n"
        "2) Нажать Enter\n"
        "3) Перебрать заголовки карточек и найти совпадение\n"
        "4) Очистить поисковый запрос\n"
        "5) Нажать Enter повторно\n\n"
        "Ожидаемый результат:\n"
        "1) В выдаче найдена карточка с названием продукта\n"
        "2) После очистки выдача сбрасывается (карточки видны)"
    )
    def test_filters_01_search_input(self, filters: FilterComponent):
        assert LAST_PRODUCT_NAME_PATH.exists(), (
            f"Файл с названием продукта не найден: {LAST_PRODUCT_NAME_PATH}. "
            "Сначала запусти тест создания продукта."
        )
        search_query = LAST_PRODUCT_NAME_PATH.read_text(encoding="utf-8").strip()
        assert search_query, "Файл last_product_name.txt пустой"

        # 1) Ввести в поле поиска название продукта из файла
        filters.fill_search(search_query)

        # 2) Нажать Enter
        filters.press_search_enter()
        filters.page.wait_for_timeout(2000)

        # 3) Перебрать заголовки карточек и проверить совпадение
        found = filters.find_card_with_title(search_query)
        assert found, (
            f"Ни одна карточка не содержит заголовок «{search_query}»"
        )

        # 4) Очистить поисковый запрос
        filters.clear_search()

        # 5) Нажать Enter повторно
        filters.press_search_enter()
        filters.page.wait_for_timeout(2000)

        # ОР: Выдача сбросилась — карточки по-прежнему видны
        filters.check_results_unchanged()
