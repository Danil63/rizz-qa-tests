"""responses-accept-01: Обработка отклика блогера со стороны рекламодателя."""
import json
from pathlib import Path

import allure
import pytest
from playwright.sync_api import Page, expect

CAMPAIGNS_URL = "https://app.rizz.market/app/advertiser/campaigns"
LAST_CAMPAIGN_CONTEXT_PATH = Path(__file__).resolve().parents[3] / "test_data" / "last_campaign_context.json"


@pytest.mark.regression
@pytest.mark.responses
@allure.epic("Отклики рекламодателя")
@allure.feature("Обработка откликов")
@allure.story("Работа с откликом блогера в деталях кампании")
@allure.tag("Regression", "Responses", "AcceptResponse")
class TestResponsesAccept01:

    @allure.title("responses-accept-01: campaigns → детали кампании → обработка отклика danil23319")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_process_blogger_response(self, advertiser_page: Page):
        assert LAST_CAMPAIGN_CONTEXT_PATH.exists(), (
            f"Файл {LAST_CAMPAIGN_CONTEXT_PATH} не найден. "
            "Сначала запусти тест создания кампании."
        )

        ctx = json.loads(LAST_CAMPAIGN_CONTEXT_PATH.read_text(encoding="utf-8"))
        campaign_title = (ctx.get("campaign_title") or "").strip()
        assert campaign_title, "Поле campaign_title в last_campaign_context.json пустое"

        advertiser_page.goto(CAMPAIGNS_URL, wait_until="networkidle")

        # Открыть кампанию
        campaign_title_el = advertiser_page.get_by_text(campaign_title, exact=True).first
        expect(campaign_title_el).to_be_visible(timeout=15000)
        campaign_title_el.click()

        advertiser_page.wait_for_timeout(3000)
        details_heading = advertiser_page.get_by_role("heading", name="Детали кампании")
        expect(details_heading).to_be_visible(timeout=10000)

        responders_count = advertiser_page.get_by_text("количество откликнувшихся блогеров", exact=False).first
        expect(responders_count).to_be_visible(timeout=10000)
        responders_count.click()

        # Простой while: если danil23319 не найден/не виден -> refresh и повтор
        max_retries = 12  # 12 * 5s = 60s
        found = False

        for _ in range(max_retries):
            danil_text = advertiser_page.locator("p", has_text="danil23319").first
            try:
                expect(danil_text).to_be_visible(timeout=2000)
                found = True
                break
            except Exception:
                advertiser_page.wait_for_timeout(5000)
                advertiser_page.reload(wait_until="networkidle")

                campaign_title_el = advertiser_page.get_by_text(campaign_title, exact=True).first
                expect(campaign_title_el).to_be_visible(timeout=10000)
                campaign_title_el.click()

                advertiser_page.wait_for_timeout(3000)
                details_heading = advertiser_page.get_by_role("heading", name="Детали кампании")
                expect(details_heading).to_be_visible(timeout=10000)

                responders_count = advertiser_page.get_by_text("количество откликнувшихся блогеров", exact=False).first
                expect(responders_count).to_be_visible(timeout=10000)
                responders_count.click()

        assert found, "Текст 'danil23319' не появился в списке откликов за отведённое время"

        # Фокус + принять
        danil_text = advertiser_page.locator("p", has_text="danil23319").first
        danil_text.scroll_into_view_if_needed()
        danil_text.click()

        accept_button = advertiser_page.get_by_role("button", name="Принять").first
        expect(accept_button).to_be_visible(timeout=10000)
        expect(accept_button).to_be_enabled(timeout=10000)
        accept_button.click()

        # После принятия блогер исчезает из списка
        expect(advertiser_page.locator("p", has_text="danil23319").first).not_to_be_visible(timeout=15000)
