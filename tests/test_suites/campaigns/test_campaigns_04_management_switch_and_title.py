"""campaigns-04: Проверка отображения кампании после переключения фильтра ведения.

Сценарий:
    1) Открыть /app/advertiser/campaigns
    2) Проверить, что таб «Активные» выбран по умолчанию
    3) В dropdown фильтра ведения выбрать «На ведении»
    4) Затем выбрать «Самостоятельно»
    5) Проверить, что в списке есть кампания с заголовком из отдельного файла
"""
from pathlib import Path

import allure
import pytest
from playwright.sync_api import expect

from tests.pages.campaigns_page import CampaignsPage

LAST_CAMPAIGN_TITLE_PATH = Path(__file__).resolve().parents[2] / "test_data" / "last_campaign_title.txt"


@pytest.mark.regression
@pytest.mark.campaigns
@allure.epic("Кампании рекламодателя")
@allure.feature("Фильтрация кампаний")
@allure.story("Переключение фильтра ведения и проверка заголовка")
@allure.tag("Regression", "Campaigns", "Filters")
class TestCampaigns04:
    @allure.title("campaigns-04: На ведении → Самостоятельно → проверка заголовка кампании")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_campaigns_04_management_switch_and_title(self, campaigns_page: CampaignsPage):
        assert LAST_CAMPAIGN_TITLE_PATH.exists(), (
            f"Файл с заголовком не найден: {LAST_CAMPAIGN_TITLE_PATH}. "
            "Сначала запусти тест создания кампании campaigns-02."
        )
        expected_title = LAST_CAMPAIGN_TITLE_PATH.read_text(encoding="utf-8").strip()
        assert expected_title, "Файл last_campaign_title.txt пустой"

        # 1-2) Страница открыта, таб «Активные» выбран
        campaigns_page.check_active_tab_selected()

        # 3) Выбрать «На ведении»
        campaigns_page.select_management_filter("На ведении")
        expect(campaigns_page.filter_management).to_contain_text("На ведении")

        # 4) Выбрать «Самостоятельно»
        campaigns_page.select_management_filter("Самостоятельно")
        expect(campaigns_page.filter_management).to_contain_text("Самостоятельно")

        # 5) Проверить кампанию по заголовку
        campaign_title = campaigns_page.page.get_by_role("link", name=expected_title, exact=True)
        expect(campaign_title).to_be_visible()
