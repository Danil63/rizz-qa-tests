"""POM: Базовая страница — общий интерфейс для всех страниц."""
import re
from typing import Pattern

from playwright.sync_api import Page, expect


class BasePage:
    URL: str = ""

    def __init__(self, page: Page):
        self.page = page

    def visit(self, url: str) -> "BasePage":
        self.page.goto(url, wait_until="networkidle")
        return self

    def navigate(self) -> "BasePage":
        self.page.goto(self.URL, wait_until="networkidle")
        return self

    def reload(self) -> None:
        self.page.reload(wait_until="domcontentloaded")

    def get_current_url(self) -> str:
        return self.page.url

    def wait(self, ms: int = 1000) -> None:
        self.page.wait_for_timeout(ms)

    def check_current_url(self, expected_url: Pattern[str]) -> None:
        expect(self.page).to_have_url(expected_url)

    def expect_url_contains(self, pattern: str, timeout: int = 10000) -> None:
        expect(self.page).to_have_url(re.compile(pattern), timeout=timeout)

    def expect_heading(self, name: str) -> None:
        expect(self.page.get_by_role("heading", name=name)).to_be_visible()
