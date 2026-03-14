"""POM: Базовая страница — общий интерфейс для всех страниц."""

import re
from typing import Pattern

from playwright.sync_api import Locator, Page, expect


class BasePage:
    """Базовый Page Object — наследуется всеми страницами."""

    URL: str = ""

    def __init__(self, page: Page):
        self.page = page

    # ── Навигация ─────────────────────────────────────────────

    def visit(self, url: str | None = None) -> "BasePage":
        """Открыть URL. Без аргументов — использует self.URL."""
        target = url or self.URL
        self.page.goto(target, wait_until="networkidle")
        return self

    def navigate(self) -> "BasePage":
        """Перейти на страницу по URL класса."""
        self.page.goto(self.URL, wait_until="networkidle")
        return self

    def reload(self) -> None:
        """Перезагрузить страницу."""
        self.page.reload(wait_until="domcontentloaded")

    def get_current_url(self) -> str:
        return self.page.url

    def wait(self, ms: int = 1000) -> None:
        self.page.wait_for_timeout(ms)

    # ── Стабильные взаимодействия (Page Factory) ──────────────

    def wait_for_element(
        self, locator: Locator, state: str = "visible", timeout: int = 10000
    ) -> None:
        """Ждать нужного состояния элемента: visible / hidden / attached / detached."""
        locator.wait_for(state=state, timeout=timeout)

    def wait_for_hidden(self, locator: Locator, timeout: int = 10000) -> None:
        """Ждать пока элемент исчезнет (спиннер, оверлей, лоадер)."""
        locator.wait_for(state="hidden", timeout=timeout)

    def wait_for_load(self, state: str = "domcontentloaded") -> None:
        """Ждать загрузки страницы. Заменяет wait(ms).
        Варианты state: domcontentloaded | load | networkidle."""
        self.page.wait_for_load_state(state)

    def safe_click(self, locator: Locator, timeout: int = 10000) -> None:
        """Клик после скролла к элементу и ожидания кликабельности."""
        locator.scroll_into_view_if_needed()
        locator.click(timeout=timeout)

    def safe_fill(self, locator: Locator, value: str, timeout: int = 10000) -> None:
        """Fill после ожидания видимости элемента."""
        locator.wait_for(state="visible", timeout=timeout)
        locator.fill(value)

    def is_visible(self, locator: Locator) -> bool:
        """Проверить видимость без броска исключения. Возвращает True/False."""
        return locator.is_visible()

    # ── Проверки ──────────────────────────────────────────────

    def check_current_url(self, expected_url: Pattern[str]) -> None:
        """Проверить что текущий URL соответствует паттерну."""
        expect(self.page).to_have_url(expected_url)

    def expect_url_contains(self, pattern: str, timeout: int = 10000) -> None:
        """Проверить что URL содержит паттерн."""
        expect(self.page).to_have_url(re.compile(pattern), timeout=timeout)

    def expect_heading(self, name: str) -> None:
        """Проверить наличие заголовка."""
        expect(self.page.get_by_role("heading", name=name)).to_be_visible()

    def expect_visible(self, locator: Locator, timeout: int = 10000) -> None:
        """Проверить что элемент видим."""
        expect(locator).to_be_visible(timeout=timeout)

    def expect_hidden(self, locator: Locator, timeout: int = 10000) -> None:
        """Проверить что элемент скрыт."""
        expect(locator).to_be_hidden(timeout=timeout)
