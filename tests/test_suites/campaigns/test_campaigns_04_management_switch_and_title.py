"""campaigns-04: Проверка отображения кампании после переключения фильтра ведения.

Сценарий:
    1) Открыть /app/advertiser/campaigns
    2) Проверить, что таб «Активные» выбран по умолчанию
    3) В dropdown фильтра ведения выбрать «На ведении»
    4) Затем выбрать «Самостоятельно»
    5) Проверить, что в списке есть кампания с заголовком из отдельного файла
"""
import json
from pathlib import Path

import allure
import pytest
from playwright.sync_api import Page, expect

from tests.pages.campaigns_page import CampaignsPage

LAST_CAMPAIGN_CONTEXT_PATH = Path(__file__).resolve().parents[2] / "test_data" / "last_campaign_context.json"


@pytest.mark.regression
@pytest.mark.campaigns
@allure.epic("Кампании рекламодателя")
@allure.feature("Фильтрация кампаний")
@allure.story("Переключение фильтра ведения и проверка заголовка")
@allure.tag("Regression", "Campaigns", "Filters")
class TestCampaigns04:
    @allure.title("campaigns-04: На ведении → Самостоятельно → проверка заголовка кампании")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_campaigns_04_management_switch_and_title(
        self, campaigns_page: CampaignsPage, page: Page,
    ):
        assert LAST_CAMPAIGN_CONTEXT_PATH.exists(), (
            f"Файл с контекстом кампании не найден: {LAST_CAMPAIGN_CONTEXT_PATH}. "
            "Сначала запусти тест создания кампании campaigns-02."
        )
        ctx = json.loads(LAST_CAMPAIGN_CONTEXT_PATH.read_text(encoding="utf-8"))
        expected_title = (ctx.get("campaign_title") or "").strip()
        assert expected_title, "Поле campaign_title в last_campaign_context.json пустое"

        # 1-2) Страница открыта, таб «Активные» выбран
        campaigns_page.check_active_tab_selected()

        # 3) Выбрать «На ведении»
        campaigns_page.select_management_filter("На ведении")
        expect(campaigns_page.filter_management).to_contain_text("На ведении")
        page.wait_for_timeout(1500)

        # 4) Выбрать «Самостоятельно»
        campaigns_page.select_management_filter("Самостоятельно")
        expect(campaigns_page.filter_management).to_contain_text("Самостоятельно")
        page.wait_for_timeout(1500)

        # 5) Проверить кампанию по заголовку (ищем по тексту, не только по role=link)
        campaign_element = page.locator(f"text='{expected_title}'").first
        expect(campaign_element).to_be_visible(timeout=10000)
