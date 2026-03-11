"""responses-05-cpm: Отправка отклика на кампанию с оплатой за просмотры (CPM)."""

import json
import time
from pathlib import Path

import allure
import pytest
from playwright.sync_api import Page

from tests.pages.send_response_page import SendResponsePage

LAST_SERVICE_META = (
    Path(__file__).resolve().parents[3] / "test_data" / "last_service_meta.json"
)
CPM_CAMPAIGN_CONTEXT_PATH = (
    Path(__file__).resolve().parents[3] / "test_data" / "cpm_campaign_context.json"
)


@pytest.mark.regression
@pytest.mark.responses
@allure.epic("Маркет блогера")
@allure.feature("Отклики")
@allure.story("Отправка отклика за просмотры (CPM)")
@allure.tag("Regression", "Responses", "CPM", "SendResponse")
class TestResponsesSend05CPM:
    @allure.title("responses-send-05: creator market → поиск → отклик за просмотры (CPM)")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_send_response_cpm(self, blogger_page: Page):
        assert LAST_SERVICE_META.exists(), (
            f"Файл {LAST_SERVICE_META} не найден. "
            "Сначала запусти тест создания продукта."
        )
        product_meta = json.loads(LAST_SERVICE_META.read_text(encoding="utf-8"))
        product_name = (product_meta.get("name") or "").strip()
        assert product_name, "Поле name в last_service_meta.json пустое"

        assert CPM_CAMPAIGN_CONTEXT_PATH.exists(), (
            f"Файл {CPM_CAMPAIGN_CONTEXT_PATH} не найден. "
            "Сначала запусти тест создания кампании."
        )
        cpm_context = json.loads(CPM_CAMPAIGN_CONTEXT_PATH.read_text(encoding="utf-8"))
        price_list = cpm_context.get("price", [])
        assert price_list, "Список 'price' в cpm_campaign_context.json пуст"
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

        # 2) Нажать кнопку с суммой "{price} ₽" на карточке
        page.wait_and_click_fix_price_button(price)

        # 3) Нажать "Выполнить за {price} ₽"
        page.click_execute_fix(price)

        # 4) Нажать input "Социальная сеть" (DOM до и после зафиксирован внутри метода)
        page.open_social_dropdown_with_dom_check()

        # 5) Нажать "Начать сразу за ..." (цена в кнопке рассчитывается динамически) + проверка закрытия модалки
        page.click_respond_cpm_and_check_modal_closed()

        # Неявное ожидание 3 секунды
        time.sleep(3)
