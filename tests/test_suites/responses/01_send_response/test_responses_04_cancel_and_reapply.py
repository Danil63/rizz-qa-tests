"""responses-04-cancel-and-reapply: Отмена и повторная отправка отклика на фиксированную выплату."""

import json
import time
from pathlib import Path

import allure
import pytest
from playwright.sync_api import Page

from tests.pages.cancel_and_reapply_page import CancelAndReapplyPage

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
@allure.story("Повторная отправка отклика на фиксированную выплату")
@allure.tag("Regression", "Responses", "Fix", "CancelAndReapply")
class TestResponsesSend02:
    @allure.title(
        "responses-send-04: creator market → cancel → reapply fix response"
    )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_cancel_and_reapply_response_fix(self, blogger_page: Page):
        assert LAST_PRODUCT_TWO_META.exists(), (
            f"Файл {LAST_PRODUCT_TWO_META} не найден. "
            "Сначала запусти тест создания продукта."
        )
        product_meta = json.loads(LAST_PRODUCT_TWO_META.read_text(encoding="utf-8"))
        product_name = (product_meta.get("name") or "").strip()
        assert product_name, "Поле name в last_product_two_meta.json пустое"

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

        page = CancelAndReapplyPage(blogger_page)
        page.open()

        # 1) Поиск продукта на странице маркет
        page.search_product_and_submit(product_name)
        page.wait_and_check_product_title(product_name)

        # 2) Нажать кнопку с суммой "{price} ₽" на карточке (вместо "Бартер")
        page.wait_and_click_fix_price_button(price)

        # 3) Нажать "Отменить отклик"
        page.wait_and_click_cancel_response()

        # 4) Нажать "Выполнить за {price} ₽"
        page.click_execute_fix(price)

        # 5) Нажать input "Социальная сеть" (DOM до и после зафиксирован внутри метода)
        page.open_social_dropdown_with_dom_check()

        # 6) Выбрать "crazy.6.3" (DOM после зафиксирован внутри метода)
        page.select_crazy_account()

        # 7) Нажать "Откликнуться за {price} ₽" + неявное ожидание 3 сек + проверка закрытия модалки
        page.click_respond_fix_and_check_modal_closed(price)

        # Неявное ожидание 3 секунды
        time.sleep(3)
