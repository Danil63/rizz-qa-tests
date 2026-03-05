"""Фикстуры для тестов интеграций.

Fixtures blogger_page и advertiser_page переопределены локально:
после загрузки cookies браузер НЕ переходит на market/campaigns —
каждый тест сам открывает нужную страницу интеграции.
"""

import json
import os
from pathlib import Path

import pytest
from playwright.sync_api import Page

BLOGGER_STATE = Path(__file__).resolve().parents[2] / "stage" / "blogger_state.json"
ADVERTISER_STATE = (
    Path(__file__).resolve().parents[2] / "stage" / "advertiser_state.json"
)

BLOGGER_PHONE = "9938854791"
BLOGGER_PASSWORD = "89087814701"
ADVERTISER_PHONE = "79087814701"
ADVERTISER_PASSWORD = "89087814701"


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
        "headless": os.getenv("PW_HEADLESS", "0") == "1",
    }


@pytest.fixture()
def blogger_page(page: Page) -> Page:
    """Авторизация блогера без загрузки market-страницы.

    Добавляет cookies в контекст, после чего тест сам навигирует
    напрямую на страницу интеграции.
    """
    if BLOGGER_STATE.exists():
        state = json.loads(BLOGGER_STATE.read_text(encoding="utf-8"))
        cookies = state.get("cookies", [])
        if cookies:
            page.context.add_cookies(cookies)
    else:
        from tests.flows.auth_flow import AuthFlow

        AuthFlow(page).login_with_phone(BLOGGER_PHONE, BLOGGER_PASSWORD)
    return page


@pytest.fixture()
def advertiser_page(page: Page) -> Page:
    """Авторизация рекламодателя без загрузки campaigns-страницы.

    Добавляет cookies в контекст, после чего тест сам навигирует
    напрямую на страницу интеграции.
    """
    if ADVERTISER_STATE.exists():
        state = json.loads(ADVERTISER_STATE.read_text(encoding="utf-8"))
        cookies = state.get("cookies", [])
        if cookies:
            page.context.add_cookies(cookies)
    else:
        from tests.flows.auth_flow import AuthFlow

        AuthFlow(page).login_with_phone(ADVERTISER_PHONE, ADVERTISER_PASSWORD)
    return page
