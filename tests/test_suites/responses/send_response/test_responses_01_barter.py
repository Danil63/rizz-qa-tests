"""responses-01: Отклик на бартер — полный флоу.

Сценарий:
    1) Старт со страницы https://app.rizz.market/app/creator/market (через fixture)
    2) Найти карточку по заголовку из last_product_name.txt
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

from tests.components.market_components.barter_response_component import BarterResponseComponent
from tests.pages.market_page import MarketPage

LAST_PRODUCT_NAME_PATH = Path(__file__).resolve().parents[3] / "test_data" / "last_product_name.txt"


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
        assert LAST_PRODUCT_NAME_PATH.exists(), (
            f"Файл {LAST_PRODUCT_NAME_PATH} не найден. "
            "Сначала запусти тест создания кампании (campaigns-02)."
        )
        product_name = LAST_PRODUCT_NAME_PATH.read_text(encoding="utf-8").strip()
        assert product_name, "Файл last_product_name.txt пустой"

        allure.attach(product_name, name="Название продукта", attachment_type=allure.attachment_type.TEXT)

        # Сужаем выдачу по точному заголовку кампании через поле поиска
        with allure.step(f'Поиск продукта через поле "Поиск": "{product_name}"'):
            market_page.search(product_name)
            page.wait_for_timeout(1200)

        with allure.step(f'Поиск карточки с заголовком "{product_name}"'):
            card = page.locator(".rounded-xl.bg-white.p-1", has=page.locator("h3", has_text=product_name)).first
            if card.count() == 0:
                visible_titles = page.locator(".rounded-xl.bg-white.p-1 h3").all_text_contents()
                allure.attach(
                    "\n".join(t.strip() for t in visible_titles if t and t.strip()) or "<пусто>",
                    name="Заголовки карточек на странице",
                    attachment_type=allure.attachment_type.TEXT,
                )
            expect(card).to_be_visible(timeout=15000)

        with allure.step('Нажатие кнопки «Бартер» на карточке'):
            barter_button = card.get_by_role("button", name="Бартер")
            expect(barter_button).to_be_visible()
            barter_button.click()

        barter_response = BarterResponseComponent(page)
        barter_response.prepare_barter_form()
        barter_response.select_social_network("danil23319")
        barter_response.click_respond_barter()

        barter_response.check_success_banner_visible()
        barter_response.check_success_text_visible()
        barter_response.check_cancel_button_visible()
