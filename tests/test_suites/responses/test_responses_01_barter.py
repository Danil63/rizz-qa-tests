"""responses-01: Отклик на бартер — полный флоу.

Сценарий:
    1) Старт с маркета на URL с фильтрами (через fixture)
    2) Найти карточку по заголовку из last_campaign_title.txt
    3) Нажать кнопку «Бартер» на карточке
    4) Нажать «Выполнить за бартер»
    5) В dropdown «Социальная сеть» выбрать «danil23319»
    6) Нажать «Откликнуться на бартер»
    7) Проверить баннер «Отклик отправлен»
    8) Проверить текст «Отклик на бартер отправлен»
    9) Проверить кнопку «Отменить отклик"
"""
from pathlib import Path

import allure
import pytest
from playwright.sync_api import Page, expect

from tests.components.market_components.barter_response_component import BarterResponseComponent
from tests.pages.market_page import MarketPage

LAST_CAMPAIGN_TITLE_PATH = Path(__file__).resolve().parents[2] / "test_data" / "last_campaign_title.txt"


@pytest.mark.regression
@pytest.mark.responses
@allure.epic("Маркет блогера")
@allure.feature("Отклики")
@allure.story("Отклик на бартер")
@allure.tag("Regression", "Responses", "Barter")
class TestResponses01:
    """responses-01: Отклик на бартер — от нажатия кнопки до баннера успеха."""

    @allure.title(
        "responses-01: Маркет → карточка → Бартер → Выполнить за бартер → "
        "выбрать соцсеть → Откликнуться → проверка баннера"
    )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_responses_01_barter(
        self,
        market_page: MarketPage,
        page: Page,
    ):
        assert LAST_CAMPAIGN_TITLE_PATH.exists(), (
            f"Файл {LAST_CAMPAIGN_TITLE_PATH} не найден. "
            "Сначала запусти тест создания кампании (campaigns-02)."
        )
        campaign_title = LAST_CAMPAIGN_TITLE_PATH.read_text(encoding="utf-8").strip()
        assert campaign_title, "Файл last_campaign_title.txt пустой"

        allure.attach(campaign_title, name="Заголовок кампании", attachment_type=allure.attachment_type.TEXT)

        # Стартовая страница уже открыта в fixture: tests/test_suites/responses/conftest.py

        with allure.step(f'Поиск карточки с заголовком "{campaign_title}"'):
            card = page.locator(".rounded-xl.bg-white.p-1", has=page.locator("h3", has_text=campaign_title))
            expect(card).to_be_visible(timeout=15000)

        with allure.step('Нажатие кнопки «Бартер» на карточке'):
            barter_button = card.get_by_role("button", name="Бартер")
            expect(barter_button).to_be_visible()
            barter_button.click()

        barter_response = BarterResponseComponent(page)
        barter_response.click_execute_barter()
        barter_response.select_social_network("danil23319")
        barter_response.click_respond_barter()

        barter_response.check_success_banner_visible()
        barter_response.check_success_text_visible()
        barter_response.check_cancel_button_visible()
