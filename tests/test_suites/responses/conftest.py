"""Фикстуры для тестов откликов на бартер."""
import pytest
from playwright.sync_api import Page

from tests.pages.market_page import MarketPage


MARKET_URL_WITH_FILTERS = (
    "https://app.rizz.market/app/creator/market"
    "?sortingMode=NEWEST_FIRST"
    "&socialNetworkTypes=%5B%22Instagram%22%5D"
    "&marketplaceId=%5B%22wildberries%22%5D"
    "&categoryId=%5B17%5D"
    "&rewardStrategy=%5B%22Barter%22%5D"
)


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
    """POM: страница маркета на нужном URL (авторизация через blogger_fixture)."""
    blogger_page.goto(MARKET_URL_WITH_FILTERS, wait_until="networkidle")
    page = MarketPage(blogger_page)
    page.expect_loaded()
    page.accept_cookies()
    return page
