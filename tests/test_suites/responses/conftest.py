"""Фикстуры для тестов откликов на бартер."""
import os

import pytest
from playwright.sync_api import Page

from tests.pages.market_page import MarketPage


MARKET_URL = "https://app.rizz.market/app/creator/market"


@pytest.fixture(scope="session")
def browser_context_args():
    return {
        "no_viewport": True,
        "locale": "ru-RU",
    }


@pytest.fixture(scope="session")
def browser_type_launch_args():
    return {
        "args": ["--start-maximized"],
        "headless": os.getenv("PW_HEADLESS", "0") == "1",
    }


@pytest.fixture()
def market_page(blogger_page: Page) -> MarketPage:
    """POM: старт со страницы маркета блогера (авторизация через blogger_fixture)."""
    blogger_page.goto(MARKET_URL, wait_until="networkidle")
    page = MarketPage(blogger_page)
    page.expect_loaded()
    page.accept_cookies()
    return page
