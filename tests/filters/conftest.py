"""Фикстуры для тестов фильтрации на маркете блогера."""
import allure
import pytest
from playwright.sync_api import Page

from tests.flows.auth_flow import AuthFlow
from tests.pages.market_page import MarketPage
from tests.components.market.filter_component import FilterComponent


# ── Учётные данные блогера ────────────────────────────────────

BLOGGER_PHONE = "9938854791"
BLOGGER_PASSWORD = "89087814701"


# ── Browser config ────────────────────────────────────────────

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


# ── Фикстуры ─────────────────────────────────────────────────

@pytest.fixture()
@allure.title("Авторизация как блогер и открытие маркета")
def blogger_market(page: Page) -> Page:
    """Авторизоваться как блогер, открыть маркет, принять cookie."""
    auth = AuthFlow(page)
    auth.login_with_phone(BLOGGER_PHONE, BLOGGER_PASSWORD)

    market = MarketPage(page)
    market.expect_loaded()
    market.accept_cookies()

    return page


@pytest.fixture()
def market_page(blogger_market: Page) -> MarketPage:
    """POM: страница маркета (уже авторизован)."""
    return MarketPage(blogger_market)


@pytest.fixture()
def filters(blogger_market: Page) -> FilterComponent:
    """PCO: компонент фильтров (уже авторизован на маркете)."""
    return FilterComponent(blogger_market)
