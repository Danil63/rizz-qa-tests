"""responses-05-cpm: Отправка отклика на кампанию с оплатой за просмотры (CPM)."""

import json
import time
from pathlib import Path

import pytest
from playwright.sync_api import Page

from tests.pages.send_response_page import SendResponsePage

LAST_SERVICE_META = (
    Path(__file__).resolve().parents[3] / "test_data" / "last_service_meta.json"
)
CPM_CAMPAIGN_CONTEXT_PATH = (
    Path(__file__).resolve().parents[3] / "test_data" / "cpm_campaign_context.json"
)


@pytest.mark.skip(reason="Временно отключён")
@pytest.mark.regression
@pytest.mark.responses
class TestResponsesSend05CPM:
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
        max_payout = cpm_context.get("price")
        assert max_payout is not None, "Поле 'price' в cpm_campaign_context.json отсутствует"
        max_payout = str(max_payout)

        page = SendResponsePage(blogger_page)
        page.open()

        # 1) Поиск продукта на странице маркет
        page.search_product_and_submit(product_name)
        page.wait_and_check_product_title(product_name)

        # 2) Нажать CPM-кнопку "{rate} ₽ за каждую 1К" на карточке
        page.wait_and_click_cpm_button()

        # 3) Нажать "Начать сразу за ..." (цена рассчитывается динамически),
        #    подождать 3 секунды, нажать повторно и ждать закрытия модалки
        page.click_respond_cpm_and_check_modal_closed()

        # Неявное ожидание 3 секунды
        time.sleep(3)
