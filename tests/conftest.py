"""Глобальные фикстуры проекта."""
import platform
import shutil
import sys
from pathlib import Path

import allure
import pytest
from playwright.sync_api import Page

# Импорт фикстур из fixtures/
from tests.fixtures.blogger_fixture import blogger_page  # noqa: F401
from tests.fixtures.advertiser_fixture import advertiser_page  # noqa: F401


@pytest.fixture(autouse=True)
def ensure_page_ready_before_test(request):
    """Гарантировать, что страница догружена перед стартом каждого теста.

    Работает для тестов, где используется стандартная playwright-фикстура `page`
    (включая проксирующие фикстуры blogger_page / advertiser_page).
    """
    try:
        page: Page = request.getfixturevalue("page")
    except Exception:
        # Тесты без page пропускаем
        return

    try:
        # Если страница уже открыта фикстурами — дожидаемся стабильного состояния.
        page.wait_for_load_state("domcontentloaded", timeout=15000)
        page.wait_for_load_state("networkidle", timeout=15000)
    except Exception:
        # Не валим тест на системном ожидании; целевые ожидания остаются в сценариях.
        pass


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
    for cache_dir in root.rglob("__pycache__"):
        shutil.rmtree(cache_dir, ignore_errors=True)

    pytest_cache = root / ".pytest_cache"
    if pytest_cache.exists():
        shutil.rmtree(pytest_cache, ignore_errors=True)

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
            pass
