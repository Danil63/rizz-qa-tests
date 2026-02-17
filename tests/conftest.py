"""Глобальные фикстуры проекта."""
import allure
import pytest
from playwright.sync_api import Page


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
