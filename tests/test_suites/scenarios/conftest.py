"""Фикстуры для сценарных тестов.

Переопределяем page и advertiser_page на scope=class,
чтобы regress (scope=class) мог их использовать.
Вся цепочка: class_page → advertiser_page → regress — scope=class.
"""
import pytest
from playwright.sync_api import BrowserType, Browser, BrowserContext, Page

from tests.flows.auth_flow import AuthFlow
from tests.pages.campaigns_page import CampaignsPage


# ── Учётные данные ────────────────────────────────────────────

ADVERTISER_PHONE = "9087814701"
ADVERTISER_PASSWORD = "89087814701"


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


# ── Class-scoped browser chain ────────────────────────────────

@pytest.fixture(scope="class")
def class_browser(browser_type: BrowserType, browser_type_launch_args: dict) -> Browser:
    """Браузер на весь класс."""
    browser = browser_type.launch(**browser_type_launch_args)
    yield browser
    browser.close()


@pytest.fixture(scope="class")
def class_context(class_browser: Browser, browser_context_args: dict) -> BrowserContext:
    """Контекст браузера на весь класс."""
    context = class_browser.new_context(**browser_context_args)
    yield context
    context.close()


@pytest.fixture(scope="class")
def class_page(class_context: BrowserContext) -> Page:
    """Страница на весь класс."""
    page = class_context.new_page()
    yield page
    page.close()


# ── Class-scoped advertiser_page (переопределение) ────────────

@pytest.fixture(scope="class")
def advertiser_page(class_page: Page) -> Page:
    """Авторизация рекламодателя — scope=class.

    Переопределяет function-scoped advertiser_page из корневого conftest.
    Используется в regress fixture.
    """
    auth = AuthFlow(class_page)
    auth.login_with_phone(ADVERTISER_PHONE, ADVERTISER_PASSWORD)
    CampaignsPage(class_page).expect_loaded()

    cookie_btn = class_page.get_by_role("button", name="Принять cookie")
    if cookie_btn.is_visible(timeout=3000):
        cookie_btn.click()

    return class_page
