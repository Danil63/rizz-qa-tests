"""POM: Базовая страница — общий интерфейс для всех страниц."""
import re
from playwright.sync_api import Page, expect


class BasePage:
    """Базовый Page Object — наследуется всеми страницами."""

    URL: str = ""

    def __init__(self, page: Page):
        self.page = page

    def navigate(self) -> "BasePage":
        """Перейти на страницу по URL."""
        self.page.goto(self.URL)
        return self

    def get_current_url(self) -> str:
        return self.page.url

    def reload(self) -> None:
        self.page.reload()

    def wait(self, ms: int = 1000) -> None:
        self.page.wait_for_timeout(ms)

    def expect_url_contains(self, pattern: str, timeout: int = 10000) -> None:
        expect(self.page).to_have_url(re.compile(pattern), timeout=timeout)

    def expect_heading(self, name: str) -> None:
        expect(self.page.get_by_role("heading", name=name)).to_be_visible()
