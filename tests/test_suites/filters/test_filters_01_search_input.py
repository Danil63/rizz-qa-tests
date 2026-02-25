"""filters-01: Поиск по input (с актуальными данными из test_data)."""
import json
from pathlib import Path

import allure
import pytest

from tests.components.market_components.filter_component import FilterComponent

TEST_DATA_DIR = Path(__file__).resolve().parents[2] / "test_data"
LAST_PRODUCT_META_PATH = TEST_DATA_DIR / "last_product_meta.json"


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
        "1) Ввести в input название продукта из last_product_meta.json\n"
        "2) Нажать Enter\n"
        "3) Перебрать заголовки карточек и найти совпадение\n"
        "4) Очистить поисковый запрос\n"
        "5) Нажать Enter повторно\n\n"
        "Ожидаемый результат:\n"
        "1) В выдаче найдена карточка с названием продукта\n"
        "2) После очистки выдача сбрасывается (карточки видны)"
    )
    def test_filters_01_search_input(self, filters: FilterComponent):
        search_query = ""

        # Приоритет: meta.json (как более надёжный источник), затем txt
        if LAST_PRODUCT_META_PATH.exists():
            try:
                meta = json.loads(LAST_PRODUCT_META_PATH.read_text(encoding="utf-8"))
                search_query = (meta.get("name") or "").strip()
            except Exception:
                pass

        assert search_query, (
            "Не найдено название продукта в last_product_meta.json (поле name). "
            "Сначала запусти тест создания продукта."
        )
        assert "тестовая кампания" not in search_query.lower(), (
            f"Вместо названия продукта получено название кампании: {search_query}"
        )

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
