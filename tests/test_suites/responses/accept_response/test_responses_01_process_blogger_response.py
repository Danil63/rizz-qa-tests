"""responses-accept-01: Обработка отклика блогера со стороны рекламодателя."""
import json
from pathlib import Path

import allure
import pytest
from playwright.sync_api import Page

from tests.pages.campaign_details_page import CampaignDetailsPage

LAST_CAMPAIGN_CONTEXT_PATH = (
    Path(__file__).resolve().parents[3] / "test_data" / "last_campaign_context.json"
)


@pytest.mark.regression
@pytest.mark.responses
@allure.epic("Отклики рекламодателя")
@allure.feature("Обработка откликов")
@allure.story("Принятие отклика блогера в деталях кампании")
@allure.tag("Regression", "Responses", "AcceptResponse")
class TestResponsesAccept01:

    @allure.title("responses-accept-01: campaigns → детали кампании → принять отклик danil23319")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_process_blogger_response(self, advertiser_page: Page):
        assert LAST_CAMPAIGN_CONTEXT_PATH.exists(), (
            f"Файл {LAST_CAMPAIGN_CONTEXT_PATH} не найден. "
            "Сначала запусти тест создания кампании."
        )

        ctx = json.loads(LAST_CAMPAIGN_CONTEXT_PATH.read_text(encoding="utf-8"))
        campaign_title = (ctx.get("campaign_title") or "").strip()
        assert campaign_title, "Поле campaign_title в last_campaign_context.json пустое"

        page = CampaignDetailsPage(advertiser_page)
        page.open()

        page.click_campaign_title(campaign_title)
        page.wait_for_details_heading()
        page.click_responders_count()
        page.wait_for_blogger_danil()
        page.focus_blogger_danil()
        page.click_accept()
        page.wait_for_blogger_danil_hidden()
