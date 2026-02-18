"""Фикстуры для тестов создания кампаний рекламодателя.

Cookie загружаются из tests/stage/advertiser_state.json.
Генерация: python tests/stage/generate_auth.py
"""
import json
import allure
import pytest
from pathlib import Path
from playwright.sync_api import Page

from tests.pages.campaigns_page import CampaignsPage
from tests.pages.create_campaign_page import CreateCampaignPage


STORAGE_STATE_PATH = Path(__file__).parent.parent.parent / "stage" / "advertiser_state.json"


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
@allure.title("Открытие страницы создания кампании (через сохранённые cookie)")
def create_campaign_page(_load_auth, page: Page) -> CreateCampaignPage:
    """Открыть страницу создания кампании напрямую."""
    cp = CreateCampaignPage(page)
    cp.visit()
    cp.expect_loaded()
    cp.accept_cookies()
    return cp


@pytest.fixture()
@allure.title("Открытие страницы списка кампаний (через сохранённые cookie)")
def campaigns_page(_load_auth, page: Page) -> CampaignsPage:
    """Открыть страницу списка кампаний напрямую."""
    cp = CampaignsPage(page)
    cp.visit()
    cp.expect_loaded()
    cp.accept_cookies()
    return cp
