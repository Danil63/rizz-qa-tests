"""Фикстуры для тестов продуктов рекламодателя.

Cookie загружаются из tests/stage/advertiser_state.json.
Генерация: python tests/stage/generate_auth.py
"""

import json
from pathlib import Path

import pytest
from playwright.sync_api import Page

from tests.pages.create_product_page import CreateProductPage
from tests.pages.products_page import ProductsPage

STORAGE_STATE_PATH = (
    Path(__file__).parent.parent.parent / "stage" / "advertiser_state.json"
)


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
    """Подгрузить cookie рекламодателя из stage."""
    assert STORAGE_STATE_PATH.exists(), (
        f"Файл {STORAGE_STATE_PATH} не найден. "
        "Запусти: python tests/stage/generate_auth.py"
    )
    state = json.loads(STORAGE_STATE_PATH.read_text())
    for cookie in state.get("cookies", []):
        page.context.add_cookies([cookie])


@pytest.fixture()
def create_product_page(_load_auth, page: Page) -> CreateProductPage:
    """Открыть страницу создания продукта напрямую."""
    cp = CreateProductPage(page)
    cp.visit()
    cp.expect_loaded()
    cp.accept_cookies()
    return cp


@pytest.fixture()
def products_page(_load_auth, page: Page) -> ProductsPage:
    """Открыть страницу списка продуктов напрямую."""
    pp = ProductsPage(page)
    pp.visit()
    pp.expect_loaded()
    pp.accept_cookies()
    return pp
