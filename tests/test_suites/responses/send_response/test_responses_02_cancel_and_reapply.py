"""responses-send-02: Отмена и повторная отправка отклика на бартер."""
import json
from pathlib import Path

import allure
import pytest
from playwright.sync_api import Page

from tests.pages.cancel_and_reapply_page import CancelAndReapplyPage

LAST_PRODUCT_META_PATH = Path(__file__).resolve().parents[3] / "test_data" / "last_product_meta.json"


@pytest.mark.regression
@pytest.mark.responses
@allure.epic("Маркет блогера")
@allure.feature("Отклики")
@allure.story("Повторная отправка отклика на бартер")
@allure.tag("Regression", "Responses", "Barter", "SendResponse")
class TestResponsesSend02:

    @allure.title("responses-send-02: creator market → cancel → reapply barter response")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_cancel_and_reapply_response_barter(self, blogger_page: Page):
        assert LAST_PRODUCT_META_PATH.exists(), (
            f"Файл {LAST_PRODUCT_META_PATH} не найден. "
            "Сначала запусти тест создания продукта."
        )
        product_meta = json.loads(LAST_PRODUCT_META_PATH.read_text(encoding="utf-8"))
        product_name = (product_meta.get("name") or "").strip()
        assert product_name, "Поле name в last_product_meta.json пустое"

        page = CancelAndReapplyPage(blogger_page)
        page.open()

        page.search_product_and_submit(product_name)
        page.wait_and_check_product_title(product_name)
        page.wait_and_click_barter()
        page.wait_and_click_cancel_response()
        page.wait_and_click_execute_barter()
        page.wait_and_open_social_dropdown()
        page.wait_and_select_danil_account()
        page.wait_and_click_respond_barter()
        page.wait_and_check_processing_banner()
        page.wait_and_check_sent_badge()
