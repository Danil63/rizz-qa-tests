"""Глобальные фикстуры проекта."""
import platform
import shutil
import sys
from pathlib import Path

import allure
import pytest
from playwright.sync_api import Page

from tests.flows.auth_flow import AuthFlow
from tests.pages.campaigns_page import CampaignsPage

# Импорт фикстур из fixtures/
from tests.fixtures.blogger_fixture import blogger_page  # noqa: F401
from tests.fixtures.product_fixture import created_product  # noqa: F401
from tests.fixtures.campaign_fixture import created_campaign  # noqa: F401


# ── Учётные данные ────────────────────────────────────────────

ADVERTISER_PHONE = "9087814701"
ADVERTISER_PASSWORD = "89087814701"


# ── Хуки ──────────────────────────────────────────────────────

def pytest_sessionfinish(session, exitstatus):
    """Записать environment.properties + очистить кеш после прогона."""
    root = Path(session.config.rootpath)

    # ── Allure environment ────────────────────────────────────
    allure_dir = session.config.getoption("--alluredir", default=None)
    if allure_dir:
        env_file = Path(allure_dir) / "environment.properties"
        env_file.parent.mkdir(parents=True, exist_ok=True)
        env_file.write_text(
            f"URL=https://app.rizz.market\n"
            f"Browser=Chromium\n"
            f"Python={sys.version.split()[0]}\n"
            f"OS={platform.system()} {platform.release()}\n"
            f"Pytest={pytest.__version__}\n"
        )

    # ── Очистка кеша ──────────────────────────────────────────
    # __pycache__
    for cache_dir in root.rglob("__pycache__"):
        shutil.rmtree(cache_dir, ignore_errors=True)

    # .pytest_cache
    pytest_cache = root / ".pytest_cache"
    if pytest_cache.exists():
        shutil.rmtree(pytest_cache, ignore_errors=True)

    # *.pyc файлы (на всякий случай)
    for pyc in root.rglob("*.pyc"):
        pyc.unlink(missing_ok=True)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Прикрепить скриншот к Allure-отчёту при падении теста."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        try:
            page: Page | None = item.funcargs.get("page")
            if page is not None and not page.is_closed():
                allure.attach(
                    page.screenshot(),
                    name="screenshot_on_failure",
                    attachment_type=allure.attachment_type.PNG,
                )
        except Exception:
            pass  # не ломаем отчёт если скриншот не получился


# ── Фикстуры авторизации ─────────────────────────────────────

@pytest.fixture()
def advertiser_page(page: Page) -> Page:
    """Авторизоваться как рекламодатель и вернуть page."""
    auth = AuthFlow(page)
    auth.login_with_phone(ADVERTISER_PHONE, ADVERTISER_PASSWORD)
    CampaignsPage(page).expect_loaded()
    # Закрыть cookie-диалог, если появился
    cookie_btn = page.get_by_role("button", name="Принять cookie")
    if cookie_btn.is_visible(timeout=3000):
        cookie_btn.click()
    return page
