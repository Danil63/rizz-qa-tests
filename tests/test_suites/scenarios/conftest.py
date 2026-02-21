"""Фикстуры для сценарных тестов.

Переопределяем page и context на scope=class,
чтобы regress (scope=class) мог их использовать.
Один браузер на весь класс тестов.
"""
import pytest
from playwright.sync_api import BrowserType, Browser, BrowserContext, Page


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
    """Страница на весь класс — один таб для всех тестов."""
    page = class_context.new_page()
    yield page
    page.close()
