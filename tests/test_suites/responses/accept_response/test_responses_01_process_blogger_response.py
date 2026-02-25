"""responses-accept-01: Обработка отклика блогера со стороны рекламодателя."""
import json
from pathlib import Path

import allure
import pytest
from playwright.sync_api import Page, expect

WORKS_URL = "https://app.rizz.market/app/advertiser/works"
LAST_CAMPAIGN_CONTEXT_PATH = Path(__file__).resolve().parents[3] / "test_data" / "last_campaign_context.json"


@pytest.mark.regression
@pytest.mark.responses
@allure.epic("Отклики рекламодателя")
@allure.feature("Обработка откликов")
@allure.story("Работа с откликом блогера в деталях кампании")
@allure.tag("Regression", "Responses", "AcceptResponse")
class TestResponsesAccept01:

    @allure.title("responses-accept-01: works → детали кампании → обработка отклика danil23319")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_process_blogger_response(self, advertiser_page: Page):
        assert LAST_CAMPAIGN_CONTEXT_PATH.exists(), (
            f"Файл {LAST_CAMPAIGN_CONTEXT_PATH} не найден. "
            "Сначала запусти тест создания кампании."
        )

        ctx = json.loads(LAST_CAMPAIGN_CONTEXT_PATH.read_text(encoding="utf-8"))
        campaign_title = (ctx.get("campaign_title") or "").strip()
        assert campaign_title, "Поле campaign_title в last_campaign_context.json пустое"

        # Старт с авторизованным рекламодателем
        advertiser_page.goto(WORKS_URL, wait_until="networkidle")

        # Нажать на заголовок рекламной кампании из JSON
        campaign_title_el = advertiser_page.get_by_text(campaign_title, exact=True).first
        expect(campaign_title_el).to_be_visible(timeout=15000)
        campaign_title_el.click()

        # Явное ожидание 3000 мс: заголовок "Детали кампании"
        advertiser_page.wait_for_timeout(3000)
        details_heading = advertiser_page.get_by_role("heading", name="Детали кампании")
        expect(details_heading).to_be_visible(timeout=10000)

        # Нажать на блок "количество откликнувшихся блогеров"
        responders_count = advertiser_page.get_by_text("количество откликнувшихся блогеров", exact=False).first
        expect(responders_count).to_be_visible(timeout=10000)
        responders_count.click()

        # Явное ожидание текста danil23319 с retry-логикой:
        # если отклик ещё не подгрузился — обновляем страницу каждые 5 секунд
        danil_text = advertiser_page.get_by_text("danil23319", exact=False).first
        retries = 0
        max_retries = 12  # до 60 секунд ожидания

        while retries < max_retries:
            if danil_text.count() > 0 and danil_text.is_visible(timeout=1000):
                break

            retries += 1
            advertiser_page.wait_for_timeout(5000)
            advertiser_page.reload(wait_until="networkidle")

            # После reload заново открываем карточку кампании и блок откликов
            campaign_title_el = advertiser_page.get_by_text(campaign_title, exact=True).first
            expect(campaign_title_el).to_be_visible(timeout=10000)
            campaign_title_el.click()

            advertiser_page.wait_for_timeout(3000)
            expect(details_heading).to_be_visible(timeout=10000)

            responders_count = advertiser_page.get_by_text("количество откликнувшихся блогеров", exact=False).first
            expect(responders_count).to_be_visible(timeout=10000)
            responders_count.click()

            danil_text = advertiser_page.get_by_text("danil23319", exact=False).first

        expect(danil_text).to_be_visible(timeout=10000)

        # Поставить focus на тексте danil23319
        danil_text.scroll_into_view_if_needed()
        danil_text.click()

        # Нажать кнопку "Принять"
        accept_button = advertiser_page.get_by_role("button", name="Принять").first
        expect(accept_button).to_be_visible(timeout=10000)
        expect(accept_button).to_be_enabled(timeout=10000)
        accept_button.click()

        # Ожидание, пока danil23319 перестанет быть видимым
        expect(danil_text).not_to_be_visible(timeout=15000)
