"""Глобальные фикстуры проекта."""
import allure
import pytest
from playwright.sync_api import Page

from tests.flows.auth_flow import AuthFlow
from tests.pages.campaigns_page import CampaignsPage

# Импорт фикстур из fixtures/
from tests.fixtures.blogger_fixture import blogger_page  # noqa: F401


# ── Учётные данные ────────────────────────────────────────────

ADVERTISER_PHONE = "9087814701"
ADVERTISER_PASSWORD = "89087814701"


# ── Хуки ──────────────────────────────────────────────────────

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Прикрепить скриншот к Allure-отчёту при падении теста."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page: Page | None = item.funcargs.get("page")
        if page is not None:
            allure.attach(
                page.screenshot(),
                name="screenshot_on_failure",
                attachment_type=allure.attachment_type.PNG,
            )


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
