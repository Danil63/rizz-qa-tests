"""filters-04: Поиск товаров по указанному маркетплейсу."""
import allure
import pytest

from tests.components.market.filter_component import FilterComponent


@pytest.mark.regression
@pytest.mark.filters
@allure.epic("Маркет блогера")
@allure.feature("Фильтрация")
@allure.story("Фильтр по маркетплейсу")
@allure.tag("Regression", "Filters")
class TestFilters04:
    """filters-04: Поиск товаров по указанному маркетплейсу."""

    @allure.title("filters-04: Поиск товаров по указанному маркетплейсу")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description(
        "Шаги:\n"
        '1) Выбрать в dropdown "Маркетплейс" значение "ВсеИнструменты"\n\n'
        "Ожидаемый результат:\n"
        "1) Поисковая выдача фильтруется по указанному фильтру"
    )
    def test_filters_04_marketplace(self, filters: FilterComponent):
        # 1) Маркетплейс → ВсеИнструменты
        filters.select_dropdown_option("Маркетплейс", "ВсеИнструменты")

        # ОР: Выдача фильтруется
        filters.check_cards_visible()
