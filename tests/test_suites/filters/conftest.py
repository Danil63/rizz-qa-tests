"""Фикстуры для тестов фильтрации на маркете блогера.

Cookie загружаются из tests/stage/blogger_state.json.
Генерация: python tests/stage/generate_auth.py
"""
import json
import allure
import pytest
from pathlib import Path
from playwright.sync_api import Page

from tests.pages.market_page import MarketPage
from tests.components.market_components.filter_component import FilterComponent


STORAGE_STATE_PATH = Path(__file__).parent.parent.parent / "stage" / "blogger_state.json"


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
def _load_auth(page: Page):
    """Подгрузить cookie блогера из stage."""
    assert STORAGE_STATE_PATH.exists(), (
        f"Файл {STORAGE_STATE_PATH} не найден. "
        "Запусти: python tests/stage/generate_auth.py"
    )
    state = json.loads(STORAGE_STATE_PATH.read_text())
    for cookie in state.get("cookies", []):
        page.context.add_cookies([cookie])


@pytest.fixture()
@allure.title("Открытие маркета (через сохранённые cookie)")
def blogger_market(_load_auth, page: Page) -> Page:
    """Открыть маркет напрямую — авторизация из stage."""
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
