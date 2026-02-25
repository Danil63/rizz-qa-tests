"""responses-send-02: Отмена и повторная отправка отклика на бартер."""
from pathlib import Path

import allure
import pytest
from playwright.sync_api import Page

from tests.pages.cancel_and_reapply_page import CancelAndReapplyPage

TEST_DATA_DIR = Path(__file__).resolve().parents[3] / "test_data"
LAST_PRODUCT_NAME_PATH = TEST_DATA_DIR / "last_product_name.txt"
LAST_CAMPAIGN_NAME_PATH = TEST_DATA_DIR / "last_campaign_name.txt"
LAST_CAMPAIGN_TITLE_PATH = TEST_DATA_DIR / "last_campaign_title.txt"


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
        source_file = None
        for candidate in [LAST_PRODUCT_NAME_PATH, LAST_CAMPAIGN_NAME_PATH, LAST_CAMPAIGN_TITLE_PATH]:
            if candidate.exists() and candidate.read_text(encoding="utf-8").strip():
                source_file = candidate
                break

        assert source_file is not None, (
            "Не найден источник названия для поиска карточки: "
            "ожидался один из файлов last_product_name.txt / last_campaign_name.txt / last_campaign_title.txt"
        )

        product_name = source_file.read_text(encoding="utf-8").strip()

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
