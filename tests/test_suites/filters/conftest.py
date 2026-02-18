"""Фикстуры для тестов фильтрации на маркете блогера.

Авторизация выполняется ОДИН РАЗ за сессию (storage_state),
каждый тест открывает маркет напрямую без повторного логина.
"""
import json
import allure
import pytest
from pathlib import Path
from playwright.sync_api import Page, Browser, BrowserType

from tests.flows.auth_flow import AuthFlow
from tests.pages.market_page import MarketPage
from tests.components.market_components.filter_component import FilterComponent


# ── Учётные данные блогера ────────────────────────────────────

BLOGGER_PHONE = "9938854791"
BLOGGER_PASSWORD = "89087814701"
STORAGE_STATE_PATH = Path(__file__).parent / ".auth_state.json"


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


# ── Одноразовый логин → сохранение storage_state ─────────────

@pytest.fixture(scope="session", autouse=True)
def _save_auth_state(browser_type_launch_args, browser_context_args, playwright):
    """Логин один раз за сессию, сохранение cookie/storage в файл."""
    browser: Browser = playwright.chromium.launch(
        headless=False,
        args=browser_type_launch_args.get("args", []),
    )
    context = browser.new_context(**browser_context_args)
    page = context.new_page()

    auth = AuthFlow(page)
    auth.login_with_phone(BLOGGER_PHONE, BLOGGER_PASSWORD)

    market = MarketPage(page)
    market.expect_loaded()
    market.accept_cookies()

    # Сохраняем состояние авторизации
    context.storage_state(path=str(STORAGE_STATE_PATH))

    page.close()
    context.close()
    browser.close()

    yield

    # Очистка после всех тестов
    if STORAGE_STATE_PATH.exists():
        STORAGE_STATE_PATH.unlink()


# ── Фикстуры для тестов ──────────────────────────────────────

@pytest.fixture()
@allure.title("Открытие маркета (без авторизации, через storage_state)")
def blogger_market(page: Page) -> Page:
    """Открыть маркет напрямую — авторизация из storage_state."""
    # Подгружаем cookie из сохранённого состояния
    if STORAGE_STATE_PATH.exists():
        state = json.loads(STORAGE_STATE_PATH.read_text())
        for cookie in state.get("cookies", []):
            page.context.add_cookies([cookie])

    market = MarketPage(page)
    market.visit()
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
