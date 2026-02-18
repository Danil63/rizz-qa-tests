"""filters-07: Поиск товаров по указанному вознаграждению."""
import allure
import pytest

from tests.components.market.filter_component import FilterComponent


@pytest.mark.regression
@pytest.mark.filters
@allure.epic("Маркет блогера")
@allure.feature("Фильтрация")
@allure.story("Фильтр по вознаграждению")
@allure.tag("Regression", "Filters")
class TestFilters07:
    """filters-07: Поиск товаров по указанному вознаграждению."""

    @allure.title("filters-07: Поиск товаров по указанному вознаграждению")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description(
        "Шаги:\n"
        '1) Выбрать в dropdown "Вознаграждение" значение "Бартер"\n\n'
        "Ожидаемый результат:\n"
        "1) Поисковая выдача фильтруется по указанному фильтру"
    )
    def test_filters_07_reward(self, filters: FilterComponent):
        # 1) Вознаграждение → Бартер
        filters.select_dropdown_option("Вознаграждение", "Бартер")

        # ОР: Выдача фильтруется
        filters.check_cards_visible()
