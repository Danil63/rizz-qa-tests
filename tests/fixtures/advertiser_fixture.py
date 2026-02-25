"""Фикстура авторизации рекламодателя (предпочтительно через сохранённые cookies)."""
import json
from pathlib import Path

import allure
import pytest
from playwright.sync_api import Page

from tests.flows.auth_flow import AuthFlow
from tests.pages.campaigns_page import CampaignsPage


ADVERTISER_PHONE = "79087814701"
ADVERTISER_PASSWORD = "89087814701"
STORAGE_STATE_PATH = Path(__file__).parent.parent / "stage" / "advertiser_state.json"


@pytest.fixture()
@allure.title("Авторизация как рекламодатель")
def advertiser_page(page: Page) -> Page:
    """Авторизоваться как рекламодатель и вернуть page.

    1) Пытается восстановить сессию из tests/stage/advertiser_state.json
    2) Если state отсутствует/пустой — логинится по телефону/паролю
    """
    if STORAGE_STATE_PATH.exists():
        state = json.loads(STORAGE_STATE_PATH.read_text(encoding="utf-8"))
        cookies = state.get("cookies", [])
        if cookies:
            page.context.add_cookies(cookies)
        page.goto(CampaignsPage.URL, wait_until="networkidle")
        CampaignsPage(page).expect_loaded()
    else:
        auth = AuthFlow(page)
        auth.login_with_phone(ADVERTISER_PHONE, ADVERTISER_PASSWORD)
        CampaignsPage(page).expect_loaded()

    cookie_btn = page.get_by_role("button", name="Принять cookie")
    if cookie_btn.is_visible(timeout=3000):
        cookie_btn.click()

    return page
