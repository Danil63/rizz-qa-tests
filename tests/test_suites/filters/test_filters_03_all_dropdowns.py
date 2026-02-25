"""filters-03: Поиск товара с использованием всех dropdown."""
import json
from pathlib import Path

import allure
import pytest

from tests.components.market_components.filter_component import FilterComponent

LAST_CAMPAIGN_CONTEXT_PATH = Path(__file__).resolve().parents[2] / "test_data" / "last_campaign_context.json"


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
        '2) Выбрать в dropdown "Маркетплейс" значение "Ozon"\n'
        '3) Выбрать в dropdown "Категория" значение "Спорт и отдых"\n'
        '4) Выбрать в dropdown "Вознаграждение" значение "Бартер"\n'
        '5) Выбрать в dropdown "Сортировка" значение "Сначала новые"\n\n'
        "Ожидаемый результат:\n"
        "1) В поисковой выдаче отображаются карточки "
        "соответствующие выбранным фильтрам"
    )
    def test_filters_03_all_dropdowns(self, filters: FilterComponent):
        social_network = "Ig"
        marketplace = "Ozon"
        category = "Спорт и отдых"
        reward = "Бартер"

        if LAST_CAMPAIGN_CONTEXT_PATH.exists():
            try:
                ctx = json.loads(LAST_CAMPAIGN_CONTEXT_PATH.read_text(encoding="utf-8"))
                social_network = ctx.get("social_network") or social_network
                marketplace = ctx.get("marketplace") or marketplace
                category = ctx.get("category") or category
                reward = ctx.get("reward") or reward
            except Exception:
                pass

        # 1) Социальная сеть
        filters.select_dropdown_option("Социальная сеть", social_network)

        # 2) Маркетплейс
        filters.select_dropdown_option("Маркетплейс", marketplace)

        # 3) Категория
        filters.select_dropdown_option("Категория", category)

        # 4) Вознаграждение
        filters.select_dropdown_option("Вознаграждение", reward)

        # 5) Сортировка → Сначала новые
        filters.select_dropdown_option("Сортировка", "Сначала новые")

        # ОР: Дожидаемся загрузки карточек и проверяем наличие через find_card_with_title
        first_card = filters.page.locator(".rounded-xl.bg-white.p-1").first
        first_card.wait_for(state="visible", timeout=20000)
        title_text = first_card.locator("h3").first.text_content() or ""
        assert title_text, "Не удалось получить заголовок первой карточки"
        found = filters.find_card_with_title(title_text)
        assert found, f"Карточка с заголовком «{title_text}» не найдена в выдаче"
