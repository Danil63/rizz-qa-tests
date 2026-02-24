"""filters-03: Поиск товара с использованием всех dropdown."""
import allure
import pytest

from tests.components.market_components.filter_component import FilterComponent


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
        '1) Выбрать в dropdown "Социальная сеть" значение "Instagram"\n'
        '2) Выбрать в dropdown "Маркетплейс" значение "Ozon"\n'
        '3) Выбрать в dropdown "Категория" значение "Спорт и отдых"\n'
        '4) Выбрать в dropdown "Вознаграждение" значение "Бартер"\n'
        '5) Выбрать в dropdown "Сортировка" значение "Сначала новые"\n\n'
        "Ожидаемый результат:\n"
        "1) В поисковой выдаче отображаются карточки "
        "соответствующие выбранным фильтрам"
    )
    def test_filters_03_all_dropdowns(self, filters: FilterComponent):
        # 1) Социальная сеть → Instagram
        filters.select_dropdown_option("Социальная сеть", "Instagram")

        # 2) Маркетплейс → Ozon
        filters.select_dropdown_option("Маркетплейс", "Ozon")

        # 3) Категория → Спорт и отдых
        filters.select_dropdown_option("Категория", "Спорт и отдых")

        # 4) Вознаграждение → Бартер
        filters.select_dropdown_option("Вознаграждение", "Бартер")

        # 5) Сортировка → Сначала новые
        filters.select_dropdown_option("Сортировка", "Сначала новые")

        # ОР: Карточки отображаются после фильтрации
        filters.check_cards_visible()
