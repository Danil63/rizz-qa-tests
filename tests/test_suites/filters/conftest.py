"""Фикстуры для тестов фильтрации на маркете блогера.

Авторизация через blogger_fixture (логин/пароль).
"""
import allure
import pytest
from playwright.sync_api import Page

from tests.fixtures.blogger_fixture import blogger_page  # noqa: F401
from tests.pages.market_page import MarketPage
from tests.components.market_components.filter_component import FilterComponent


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
@allure.title("Открытие маркета блогера (через логин)")
def blogger_market(blogger_page: Page) -> Page:
    """Открыть маркет — авторизация через blogger_fixture."""
    market = MarketPage(blogger_page)
    market.expect_loaded()
    return blogger_page


@pytest.fixture()
def market_page(blogger_market: Page) -> MarketPage:
    """POM: страница маркета (уже авторизован)."""
    return MarketPage(blogger_market)


@pytest.fixture()
def filters(blogger_market: Page) -> FilterComponent:
    """PCO: компонент фильтров (уже авторизован на маркете)."""
    return FilterComponent(blogger_market)
