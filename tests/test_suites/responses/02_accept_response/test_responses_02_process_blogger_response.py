"""responses-accept-02: Принятие отклика блогера "Даня СЗ" со стороны рекламодателя."""

import json
from pathlib import Path

import pytest
from playwright.sync_api import Page

from tests.pages.campaign_details_page import CampaignDetailsPage

FIX_CAMPAIGN_CONTEXT_PATH = (
    Path(__file__).resolve().parents[3] / "test_data" / "fix_campaing_context.json"
)
BLOGGER_USERNAME = "Даня СЗ"


@pytest.mark.regression
@pytest.mark.responses
class TestResponsesAccept02:
    def test_process_blogger_response(self, advertiser_page: Page):
        assert FIX_CAMPAIGN_CONTEXT_PATH.exists(), (
            f"Файл {FIX_CAMPAIGN_CONTEXT_PATH} не найден. "
            "Сначала запусти тест создания кампании."
        )

        ctx = json.loads(FIX_CAMPAIGN_CONTEXT_PATH.read_text(encoding="utf-8"))
        campaign_title = (ctx.get("campaign_title") or "").strip()
        assert campaign_title, "Поле campaign_title в fix_campaing_context.json пустое"

        page = CampaignDetailsPage(advertiser_page)

        # 1) Открыть страницу кампаний
        page.open()

        # 2) Кликнуть по заголовку кампании
        page.click_campaign_title(campaign_title)

        # 3) Проверить заголовок "Детали кампании"
        page.wait_for_details_heading()

        # 4) Нажать на ссылку "Отклики"
        page.click_offers_link()

        # 5) Проверить заголовок страницы "Отклики"
        page.wait_for_offers_heading()

        # 6) Дождаться появления блогера в списке
        page.wait_for_blogger(BLOGGER_USERNAME)

        # 7) Навести курсор на карточку блогера (появляется кнопка "Принять")
        page.focus_blogger(BLOGGER_USERNAME)

        # 8) Нажать "Принять"
        page.click_accept_for_blogger(BLOGGER_USERNAME)

        page.wait(2000)

        # 9) Убедиться, что карточка блогера исчезла из списка
        page.wait_for_blogger_hidden(BLOGGER_USERNAME)
