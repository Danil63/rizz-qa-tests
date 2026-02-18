"""POM: Базовая страница — общий интерфейс для всех страниц."""
import re
from typing import Pattern

import allure
from playwright.sync_api import Page, expect


class BasePage:
    """Базовый Page Object — наследуется всеми страницами."""

    URL: str = ""

    def __init__(self, page: Page):
        self.page = page

    # ── Навигация ─────────────────────────────────────────────

    def visit(self, url: str | None = None) -> "BasePage":
        """Открыть URL. Без аргументов — использует self.URL."""
        target = url or self.URL
        with allure.step(f'Opening URL "{target}"'):
            self.page.goto(target, wait_until="networkidle")
        return self

    def navigate(self) -> "BasePage":
        """Перейти на страницу по URL класса."""
        with allure.step(f'Navigating to "{self.URL}"'):
            self.page.goto(self.URL, wait_until="networkidle")
        return self

    def reload(self) -> None:
        """Перезагрузить страницу."""
        with allure.step(f'Reloading page "{self.page.url}"'):
            self.page.reload(wait_until="domcontentloaded")

    def get_current_url(self) -> str:
        return self.page.url

    def wait(self, ms: int = 1000) -> None:
        self.page.wait_for_timeout(ms)

    # ── Проверки ──────────────────────────────────────────────

    def check_current_url(self, expected_url: Pattern[str]) -> None:
        """Проверить что текущий URL соответствует паттерну."""
        with allure.step(f'Checking URL matches pattern'):
            expect(self.page).to_have_url(expected_url)

    def expect_url_contains(self, pattern: str, timeout: int = 10000) -> None:
        """Проверить что URL содержит паттерн."""
        with allure.step(f'Checking URL contains "{pattern}"'):
            expect(self.page).to_have_url(re.compile(pattern), timeout=timeout)

    def expect_heading(self, name: str) -> None:
        """Проверить наличие заголовка."""
        with allure.step(f'Checking heading "{name}" is visible'):
            expect(self.page.get_by_role("heading", name=name)).to_be_visible()
