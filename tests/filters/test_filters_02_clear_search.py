"""filters-02: Отчистка input и повторный поиск с пустым input."""
import allure
import pytest

from tests.components.market.filter_component import FilterComponent


@pytest.mark.regression
@pytest.mark.filters
@allure.epic("Маркет блогера")
@allure.feature("Фильтрация")
@allure.story("Поиск по тексту")
@allure.tag("Regression", "Filters")
class TestFilters02:
    """filters-02: Отчистка input и повторный поиск с пустым input."""

    @allure.title("filters-02: Отчистка input и повторный поиск с пустым input")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description(
        "Шаги:\n"
        "1) Стереть ранее указанное значение в поле\n"
        '2) Нажать на "Enter"\n\n'
        "Ожидаемый результат:\n"
        "1) Поиск не запускается, выдача остаётся неизменна "
        "с прошлого запроса"
    )
    def test_filters_02_clear_search(self, filters: FilterComponent):
        # Предусловие: ввести текст чтобы было что стирать
        filters.fill_search("Гвозди для пистолета")
        filters.press_search_enter()
        filters.check_cards_visible()

        # 1) Стереть ранее указанное значение в поле
        filters.clear_search()

        # 2) Нажать на "Enter"
        filters.press_search_enter()

        # ОР: Поиск не запускается, выдача остаётся неизменна
        filters.check_results_unchanged()
