"""filters-05: Поиск товаров по указанной соц-сети."""
import allure
import pytest

from tests.components.market.filter_component import FilterComponent


@pytest.mark.regression
@pytest.mark.filters
@allure.epic("Маркет блогера")
@allure.feature("Фильтрация")
@allure.story("Фильтр по социальной сети")
@allure.tag("Regression", "Filters")
class TestFilters05:
    """filters-05: Поиск товаров по указанной соц-сети."""

    @allure.title("filters-05: Поиск товаров по указанной соц-сети")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description(
        "Шаги:\n"
        '1) Выбрать в dropdown "Социальная сеть" значение "Ig"\n\n'
        "Ожидаемый результат:\n"
        "1) Поисковая выдача фильтруется по указанному фильтру"
    )
    def test_filters_05_social_network(self, filters: FilterComponent):
        # 1) Социальная сеть → Ig
        filters.select_dropdown_option("Социальная сеть", "Ig")

        # ОР: Выдача фильтруется
        filters.check_cards_visible()
