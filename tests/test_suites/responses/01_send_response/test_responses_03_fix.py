"""responses-03-fix: Отправка отклика на фиксированную выплату."""

import json
import time
from pathlib import Path

import allure
import pytest
from playwright.sync_api import Page

from tests.pages.send_response_page import SendResponsePage

LAST_PRODUCT_TWO_META = (
    Path(__file__).resolve().parents[3] / "test_data" / "last_product_two_meta.json"
)
FIX_CAMPAIGN_CONTEXT_PATH = (
    Path(__file__).resolve().parents[3] / "test_data" / "fix_campaing_context.json"
)


@pytest.mark.regression
@pytest.mark.responses
@allure.epic("Маркет блогера")
@allure.feature("Отклики")
@allure.story("Отправка отклика на фиксированную выплату")
@allure.tag("Regression", "Responses", "Fix", "SendResponse")
class TestResponsesSend01:
    @allure.title("responses-send-01: creator market → поиск → отклик на бартер")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_send_response_barter(self, blogger_page: Page):
        assert LAST_PRODUCT_TWO_META.exists(), (
            f"Файл {LAST_PRODUCT_TWO_META} не найден. "
            "Сначала запусти тест создания продукта."
        )
        product_meta = json.loads(LAST_PRODUCT_TWO_META.read_text(encoding="utf-8"))
        product_name = (product_meta.get("name") or "").strip()
        assert product_name, "Поле name в last_product_meta.json пустое"

        assert FIX_CAMPAIGN_CONTEXT_PATH.exists(), (
            f"Файл {FIX_CAMPAIGN_CONTEXT_PATH} не найден. "
            "Сначала запусти тест создания кампании."
        )
        fix_context = json.loads(FIX_CAMPAIGN_CONTEXT_PATH.read_text(encoding="utf-8"))
        price_list = fix_context.get("price", [])
        assert price_list, "Список 'price' в fix_campaing_context.json пуст"
        price = str(price_list[-1])

        allure.attach(
            f"Продукт: {product_name}\nЦена вознаграждения: {price} ₽",
            name="Входные данные теста",
            attachment_type=allure.attachment_type.TEXT,
        )

        page = SendResponsePage(blogger_page)
        page.open()

        # 1) Поиск продукта на странице маркет
        page.search_product_and_submit(product_name)
        page.wait_and_check_product_title(product_name)

        # 2) Нажать кнопку с суммой "{price} ₽" на карточке (вместо "Бартер")
        page.wait_and_click_fix_price_button(price)

        # 3) Нажать "Выполнить за {price} ₽"
        page.click_execute_fix(price)

        # 4) Нажать input "Социальная сеть" (DOM до и после зафиксирован внутри метода)
        page.open_social_dropdown_with_dom_check()

        # 5) Выбрать "crazy.6.3" (DOM после зафиксирован внутри метода)
        page.select_crazy_account()

        # 6) Нажать "Откликнуться за {price} ₽" + неявное ожидание 3 сек + проверка закрытия модалки
        page.click_respond_fix_and_check_modal_closed(price)

        # Неявное ожидание 3 секунды
        time.sleep(3)
