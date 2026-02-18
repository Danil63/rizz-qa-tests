"""filters-01: Поиск товара с использованием input."""
import allure
import pytest

from tests.components.market.filter_component import FilterComponent


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
        # 1) Ввести в поле поиска "Гвозди для пистолета"
        filters.fill_search("Гвозди для пистолета")
        filters.press_search_enter()

        # ОР: Первая карточка содержит релевантный текст
        filters.check_first_card_contains("Гвозди")
