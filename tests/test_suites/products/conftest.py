"""Фикстуры для тестов продуктов рекламодателя.

Авторизация выполняется ОДИН РАЗ за сессию (storage_state),
каждый тест открывает страницу напрямую без повторного логина.
"""
import json
import allure
import pytest
from pathlib import Path
from playwright.sync_api import Page, Browser

from tests.flows.auth_flow import AuthFlow
from tests.pages.campaigns_page import CampaignsPage
from tests.pages.products_page import ProductsPage
from tests.pages.create_product_page import CreateProductPage


# ── Учётные данные рекламодателя ──────────────────────────────

ADVERTISER_PHONE = "9087814701"
ADVERTISER_PASSWORD = "89087814701"
STORAGE_STATE_PATH = Path(__file__).parent / ".auth_state_advertiser.json"


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
    auth.login_with_phone(ADVERTISER_PHONE, ADVERTISER_PASSWORD)

    # Ждём редирект на campaigns
    campaigns = CampaignsPage(page)
    campaigns.expect_loaded()

    # Принимаем cookie если есть
    cookie_btn = page.get_by_role("button", name="Принять cookie")
    if cookie_btn.is_visible(timeout=3000):
        cookie_btn.click()

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
def _load_auth(page: Page):
    """Подгрузить cookie авторизации рекламодателя."""
    if STORAGE_STATE_PATH.exists():
        state = json.loads(STORAGE_STATE_PATH.read_text())
        for cookie in state.get("cookies", []):
            page.context.add_cookies([cookie])


@pytest.fixture()
@allure.title("Открытие страницы создания продукта (без авторизации)")
def create_product_page(_load_auth, page: Page) -> CreateProductPage:
    """Открыть страницу создания продукта напрямую."""
    cp = CreateProductPage(page)
    cp.visit()
    cp.expect_loaded()
    cp.accept_cookies()
    return cp


@pytest.fixture()
@allure.title("Открытие страницы списка продуктов (без авторизации)")
def products_page(_load_auth, page: Page) -> ProductsPage:
    """Открыть страницу списка продуктов напрямую."""
    pp = ProductsPage(page)
    pp.visit()
    pp.expect_loaded()
    pp.accept_cookies()
    return pp
