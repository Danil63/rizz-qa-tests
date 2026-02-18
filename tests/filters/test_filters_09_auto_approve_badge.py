"""filters-09: Отображение маркировки "Автоодобрение" в карточке товара."""
import allure
import pytest

from tests.components.market.filter_component import FilterComponent


@pytest.mark.regression
@pytest.mark.filters
@allure.epic("Маркет блогера")
@allure.feature("Фильтрация")
@allure.story("Бейджи карточек")
@allure.tag("Regression", "Filters")
class TestFilters09:
    """filters-09: Отображение маркировки "Автоодобрение" в карточке товара."""

    @allure.title('filters-09: Отображение плашки "Автоодобрение" в карточках')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description(
        "Шаги:\n"
        "1) Осмотреть блок карточки в котором отображается "
        "стоимость товара\n\n"
        "Ожидаемый результат:\n"
        '1) В карточках товара отображается плашка "Автоодобрение"'
    )
    def test_filters_09_auto_approve_badge(self, filters: FilterComponent):
        # 1) Проверить что на странице есть карточки с плашкой "АВТООДОБРЕНИЕ"
        filters.check_badge_visible_in_cards("АВТООДОБРЕНИЕ")
