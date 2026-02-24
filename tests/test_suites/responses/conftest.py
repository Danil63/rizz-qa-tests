"""Фикстуры для тестов откликов на бартер."""
import pytest
from playwright.sync_api import Page

from tests.pages.market_page import MarketPage


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
        "headless": False,
    }


@pytest.fixture()
def market_page(blogger_page: Page) -> MarketPage:
    """POM: страница маркета (уже авторизован как блогер)."""
    return MarketPage(blogger_page)
