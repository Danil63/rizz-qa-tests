"""responses-02: Отмена отклика и повторный отклик на бартер (старт с creator market)."""
from pathlib import Path

import allure
import pytest
from playwright.sync_api import Page, expect

from tests.components.market_components.barter_response_component import BarterResponseComponent
from tests.pages.market_page import MarketPage

LAST_PRODUCT_NAME_PATH = Path(__file__).resolve().parents[3] / "test_data" / "last_product_name.txt"


@pytest.mark.regression
@pytest.mark.responses
@allure.epic("Маркет блогера")
@allure.feature("Отклики")
@allure.story("Отмена и повторный отклик на бартер")
@allure.tag("Regression", "Responses", "Barter")
class TestResponses02:

    @allure.title("responses-02: карточка → Бартер → Отменить отклик → повторный отклик")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_responses_02_cancel_and_reapply(self, market_page: MarketPage, page: Page):
        assert LAST_PRODUCT_NAME_PATH.exists(), (
            f"Файл {LAST_PRODUCT_NAME_PATH} не найден. "
            "Сначала запусти тест создания продукта."
        )
        product_name = LAST_PRODUCT_NAME_PATH.read_text(encoding="utf-8").strip()
        assert product_name, "Файл last_product_name.txt пустой"

        with allure.step(f'Найти карточку товара с заголовком "{product_name}"'):
            market_page.search(product_name)
            page.wait_for_timeout(1200)
            product_card = page.locator(".rounded-xl.bg-white.p-1", has=page.locator("h3", has_text=product_name)).first
            expect(product_card).to_be_visible(timeout=15000)

        with allure.step("Нажать на карточку товара"):
            product_card.click()

        with allure.step('Нажать на кнопку "Бартер"'):
            barter_button = page.get_by_role("button", name="Бартер").first
            expect(barter_button).to_be_visible(timeout=10000)
            barter_button.click()

        barter_response = BarterResponseComponent(page)

        with allure.step('Нажать на кнопку "Отменить отклик"'):
            cancel_button = page.get_by_role("button", name="Отменить отклик").first
            expect(cancel_button).to_be_visible(timeout=10000)
            cancel_button.click()

        with allure.step('Явное ожидание 10 сек: кнопка "Выполнить за бартер"'):
            expect(page.get_by_role("button", name="Выполнить за бартер").first).to_be_visible(timeout=10000)

        with allure.step('Нажать на кнопку "Выполнить за бартер"'):
            barter_response.click_execute_barter()

        with allure.step('Выбрать соцсеть "danil23319" в dropdown'):
            barter_response.select_social_network("danil23319")

        with allure.step('Нажать на кнопку "Выполнить за бартер" в модалке'):
            submit_button = page.get_by_role("button", name="Выполнить за бартер").first
            expect(submit_button).to_be_visible(timeout=10000)
            submit_button.click()

        with allure.step('Явное ожидание появления кнопки "Отменить отклик"'):
            expect(page.get_by_role("button", name="Отменить отклик").first).to_be_visible(timeout=10000)
