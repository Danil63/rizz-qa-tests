"""responses-01: Отклик на бартер — полный флоу.

Сценарий:
    1) Открыть маркет с фильтрами (Instagram, Wildberries, категория 17, Бартер, сортировка по новизне)
    2) Найти карточку по заголовку из last_campaign_title.txt
    3) Нажать кнопку «Бартер» на карточке
    4) Нажать «Выполнить за бартер»
    5) В dropdown «Социальная сеть» выбрать «danil23319»
    6) Нажать «Откликнуться на бартер»
    7) Проверить баннер «Отклик отправлен»
    8) Проверить текст «Отклик на бартер отправлен»
    9) Проверить кнопку «Отменить отклик»
"""
from pathlib import Path

import allure
import pytest
from playwright.sync_api import Page, expect

from tests.pages.market_page import MarketPage
from tests.components.market_components.barter_response_component import BarterResponseComponent

LAST_CAMPAIGN_TITLE_PATH = Path(__file__).resolve().parents[2] / "test_data" / "last_campaign_title.txt"

MARKET_URL_WITH_FILTERS = (
    "https://app.rizz.market/app/creator/market"
    "?socialNetworkTypes=%5B%22Instagram%22%5D"
    "&marketplaceId=%5B%22wildberries%22%5D"
    "&categoryId=%5B17%5D"
    "&rewardStrategy=%5B%22Barter%22%5D"
    "&sortingMode=NEWEST_FIRST"
)


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
    @allure.description(
        "Шаги:\n"
        "1) Открыть маркет с преднастроенными фильтрами\n"
        "2) Найти карточку по заголовку из last_campaign_title.txt\n"
        "3) Нажать «Бартер» на карточке\n"
        "4) Нажать «Выполнить за бартер»\n"
        "5) В dropdown «Социальная сеть» выбрать «danil23319»\n"
        "6) Нажать «Откликнуться на бартер»\n"
        "7) Проверить баннер «Отклик отправлен»\n"
        "8) Проверить текст «Отклик на бартер отправлен»\n"
        "9) Проверить кнопку «Отменить отклик»\n\n"
        "Ожидаемый результат:\n"
        "Отображается баннер успеха с заголовком «Отклик отправлен», "
        "текстом «Отклик на бартер отправлен» и кнопкой «Отменить отклик»."
    )
    def test_responses_01_barter(
        self,
        market_page: MarketPage,
        page: Page,
    ):
        # 0) Читаем заголовок кампании
        assert LAST_CAMPAIGN_TITLE_PATH.exists(), (
            f"Файл {LAST_CAMPAIGN_TITLE_PATH} не найден. "
            "Сначала запусти тест создания кампании (campaigns-02)."
        )
        campaign_title = LAST_CAMPAIGN_TITLE_PATH.read_text(encoding="utf-8").strip()
        assert campaign_title, "Файл last_campaign_title.txt пустой"

        allure.attach(campaign_title, name="Заголовок кампании", attachment_type=allure.attachment_type.TEXT)

        # 1) Открываем маркет с фильтрами
        with allure.step("Открытие маркета с фильтрами"):
            page.goto(MARKET_URL_WITH_FILTERS, wait_until="networkidle")
            market_page.expect_loaded()
            market_page.accept_cookies()

        # 2) Находим карточку по заголовку
        with allure.step(f'Поиск карточки с заголовком "{campaign_title}"'):
            card = page.locator(".rounded-xl.bg-white.p-1", has=page.locator("h3", has_text=campaign_title))
            expect(card).to_be_visible(timeout=15000)

        # 3) Нажимаем кнопку «Бартер» на карточке
        with allure.step('Нажатие кнопки «Бартер» на карточке'):
            barter_button = card.get_by_role("button", name="Бартер")
            expect(barter_button).to_be_visible()
            barter_button.click()

        # 4-6) Работа с модалкой отклика
        barter_response = BarterResponseComponent(page)

        # 4) Нажать «Выполнить за бартер»
        barter_response.click_execute_barter()

        # 5) Выбрать соцсеть «danil23319»
        barter_response.select_social_network("danil23319")

        # 6) Нажать «Откликнуться на бартер»
        barter_response.click_respond_barter()

        # 7) Проверить баннер «Отклик отправлен»
        barter_response.check_success_banner_visible()

        # 8) Проверить текст «Отклик на бартер отправлен»
        barter_response.check_success_text_visible()

        # 9) Проверить кнопку «Отменить отклик»
        barter_response.check_cancel_button_visible()
