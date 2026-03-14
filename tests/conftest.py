"""Глобальные фикстуры проекта."""

import shutil
from pathlib import Path

import pytest
from playwright.sync_api import Page

from tests.fixtures.advertiser_fixture import advertiser_page  # noqa: F401

# Импорт фикстур из fixtures/
from tests.fixtures.blogger_fixture import blogger_page  # noqa: F401


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

    # Глобальный таймаут по умолчанию для всех expect/wait в тесте
    page.set_default_timeout(15000)

    try:
        # Если страница уже открыта фикстурами — дожидаемся стабильного состояния.
        page.wait_for_load_state("domcontentloaded", timeout=15000)
        page.wait_for_load_state("networkidle", timeout=15000)
    except Exception:
        # Не валим тест на системном ожидании; целевые ожидания остаются в сценариях.
        pass


# ── Хуки ──────────────────────────────────────────────────────


def pytest_sessionfinish(session, exitstatus):
    """Очистить кеш после прогона."""
    root = Path(session.config.rootpath)

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
    """Хук для обработки результатов теста."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        try:
            page: Page | None = item.funcargs.get("page")
            if page is not None and not page.is_closed():
                pass
        except Exception:
            pass
