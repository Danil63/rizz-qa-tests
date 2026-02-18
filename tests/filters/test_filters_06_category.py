"""filters-06: Поиск товаров по выбранной категории."""
import allure
import pytest

from tests.components.market.filter_component import FilterComponent


@pytest.mark.regression
@pytest.mark.filters
@allure.epic("Маркет блогера")
@allure.feature("Фильтрация")
@allure.story("Фильтр по категории")
@allure.tag("Regression", "Filters")
class TestFilters06:
    """filters-06: Поиск товаров по выбранной категории."""

    @allure.title("filters-06: Поиск товаров по выбранной категории")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description(
        "Шаги:\n"
        '1) Выбрать в dropdown "Категория" значение "Строительство и ремонт"\n\n'
        "Ожидаемый результат:\n"
        "1) Поисковая выдача фильтруется по указанному фильтру"
    )
    def test_filters_06_category(self, filters: FilterComponent):
        # 1) Категория → Строительство и ремонт
        filters.select_dropdown_option("Категория", "Строительство и ремонт")

        # ОР: Выдача фильтруется
        filters.check_cards_visible()
