"""Фикстура авторизации блогера."""
import pytest
from playwright.sync_api import Page

from tests.flows.auth_flow import AuthFlow
from tests.pages.market_page import MarketPage


# ── Учётные данные блогера ────────────────────────────────────

BLOGGER_PHONE = "9938854791"
BLOGGER_PASSWORD = "89087814701"


# ── Фикстура ─────────────────────────────────────────────────

@pytest.fixture()
def blogger_page(page: Page) -> Page:
    """Авторизоваться как блогер (Данил СЗ) и вернуть page."""
    auth = AuthFlow(page)
    auth.login_with_phone(BLOGGER_PHONE, BLOGGER_PASSWORD)
    MarketPage(page).expect_loaded()
    # Закрыть cookie-диалог, если появился
    cookie_btn = page.get_by_role("button", name="Принять cookie")
    if cookie_btn.is_visible(timeout=3000):
        cookie_btn.click()
    return page
