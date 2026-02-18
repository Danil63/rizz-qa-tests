"""filters-08: Поиск товара по указанным опциям кампании."""
import allure
import pytest

from tests.components.market_components.filter_component import FilterComponent


@pytest.mark.regression
@pytest.mark.filters
@allure.epic("Маркет блогера")
@allure.feature("Фильтрация")
@allure.story("Фильтр по опциям кампании")
@allure.tag("Regression", "Filters")
class TestFilters08:
    """filters-08: Поиск товара по указанным опциям кампании."""

    @allure.title("filters-08: Поиск товара по указанным опциям кампании")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description(
        "Шаги:\n"
        '1) Выбрать в dropdown "Опции кампании" значение "Автоодобрение"\n\n'
        "Ожидаемый результат:\n"
        "1) Поисковая выдача фильтруется по указанному фильтру"
    )
    def test_filters_08_campaign_options(self, filters: FilterComponent):
        # 1) Опции кампании → Автоодобрение
        filters.select_dropdown_option("Опции кампании", "Автоодобрение")

        # ОР: Выдача фильтруется
        filters.check_cards_visible()
