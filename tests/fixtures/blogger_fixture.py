"""Фикстура авторизации блогера (предпочтительно через сохранённые cookies)."""
import json
from pathlib import Path

import allure
import pytest
from playwright.sync_api import Page

from tests.flows.auth_flow import AuthFlow
from tests.pages.market_page import MarketPage


# ── Учётные данные блогера ────────────────────────────────────

BLOGGER_PHONE = "9938854791"
BLOGGER_PASSWORD = "89087814701"
STORAGE_STATE_PATH = Path(__file__).parent.parent / "stage" / "blogger_state.json"


# ── Фикстура ─────────────────────────────────────────────────

@pytest.fixture()
@allure.title("Авторизация как блогер (Данил СЗ)")
def blogger_page(page: Page) -> Page:
    """Авторизоваться как блогер и вернуть page.

    1) Пытается восстановить сессию из tests/stage/blogger_state.json
    2) Если state отсутствует — логинится по телефону/паролю
    """
    if STORAGE_STATE_PATH.exists():
        state = json.loads(STORAGE_STATE_PATH.read_text(encoding="utf-8"))
        cookies = state.get("cookies", [])
        if cookies:
            page.context.add_cookies(cookies)
        page.goto(MarketPage.URL, wait_until="networkidle")
        MarketPage(page).expect_loaded()
    else:
        auth = AuthFlow(page)
        auth.login_with_phone(BLOGGER_PHONE, BLOGGER_PASSWORD)
        MarketPage(page).expect_loaded()

    cookie_btn = page.get_by_role("button", name="Принять cookie")
    if cookie_btn.is_visible(timeout=3000):
        cookie_btn.click()

    return page
