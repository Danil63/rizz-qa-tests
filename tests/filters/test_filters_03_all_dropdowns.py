"""filters-03: Поиск товара с использованием всех dropdown."""
import allure
import pytest

from tests.components.market.filter_component import FilterComponent


@pytest.mark.regression
@pytest.mark.filters
@allure.epic("Маркет блогера")
@allure.feature("Фильтрация")
@allure.story("Комбинация фильтров")
@allure.tag("Regression", "Filters")
class TestFilters03:
    """filters-03: Поиск товара с использованием всех dropdown."""

    @allure.title("filters-03: Поиск товара с использованием всех dropdown")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description(
        "Шаги:\n"
        '1) Выбрать в dropdown "Социальная сеть" значение "Ig"\n'
        '2) Выбрать в dropdown "Маркетплейс" значение "ВсеИнструменты"\n'
        '3) Выбрать в dropdown "Категория" значение "Строительство и ремонт"\n'
        '4) Выбрать в dropdown "Вознаграждение" значение "Бартер"\n'
        '5) Выбрать в dropdown "Опции кампании" значение "Без маркировки"\n\n'
        "Ожидаемый результат:\n"
        "1) В поисковой выдаче на 1 месте отображается товар "
        "с названием релевантным запросу"
    )
    def test_filters_03_all_dropdowns(self, filters: FilterComponent):
        # 1) Социальная сеть → Ig
        filters.select_dropdown_option("Социальная сеть", "Ig")

        # 2) Маркетплейс → ВсеИнструменты
        filters.select_dropdown_option("Маркетплейс", "ВсеИнструменты")

        # 3) Категория → Строительство и ремонт
        filters.select_dropdown_option("Категория", "Строительство и ремонт")

        # 4) Вознаграждение → Бартер
        filters.select_dropdown_option("Вознаграждение", "Бартер")

        # 5) Опции кампании → Без маркировки
        filters.select_dropdown_option("Опции кампании", "Без маркировки")

        # ОР: Карточки отображаются после фильтрации
        filters.check_cards_visible()
