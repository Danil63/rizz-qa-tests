"""POM: Базовая страница — общий интерфейс для всех страниц."""

import re
from typing import Pattern

import allure
from playwright.sync_api import Page, Locator, expect


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

    # ── Стабильные взаимодействия (Page Factory) ──────────────

    def wait_for_element(
        self, locator: Locator, state: str = "visible", timeout: int = 10000
    ) -> None:
        """Ждать нужного состояния элемента: visible / hidden / attached / detached."""
        with allure.step(f'Waiting for element state="{state}"'):
            locator.wait_for(state=state, timeout=timeout)

    def wait_for_hidden(self, locator: Locator, timeout: int = 10000) -> None:
        """Ждать пока элемент исчезнет (спиннер, оверлей, лоадер)."""
        with allure.step("Waiting for element to disappear"):
            locator.wait_for(state="hidden", timeout=timeout)

    def wait_for_load(self, state: str = "domcontentloaded") -> None:
        """Ждать загрузки страницы. Заменяет wait(ms).
        Варианты state: domcontentloaded | load | networkidle."""
        with allure.step(f'Waiting for page load state="{state}"'):
            self.page.wait_for_load_state(state)

    def safe_click(self, locator: Locator, timeout: int = 10000) -> None:
        """Клик после скролла к элементу и ожидания кликабельности."""
        with allure.step("Clicking element"):
            locator.scroll_into_view_if_needed()
            locator.click(timeout=timeout)

    def safe_fill(self, locator: Locator, value: str, timeout: int = 10000) -> None:
        """Fill после ожидания видимости элемента."""
        with allure.step(f'Filling element with "{value}"'):
            locator.wait_for(state="visible", timeout=timeout)
            locator.fill(value)

    def is_visible(self, locator: Locator) -> bool:
        """Проверить видимость без броска исключения. Возвращает True/False."""
        return locator.is_visible()

    # ── Проверки ──────────────────────────────────────────────

    def check_current_url(self, expected_url: Pattern[str]) -> None:
        """Проверить что текущий URL соответствует паттерну."""
        with allure.step("Checking URL matches pattern"):
            expect(self.page).to_have_url(expected_url)

    def expect_url_contains(self, pattern: str, timeout: int = 10000) -> None:
        """Проверить что URL содержит паттерн."""
        with allure.step(f'Checking URL contains "{pattern}"'):
            expect(self.page).to_have_url(re.compile(pattern), timeout=timeout)

    def expect_heading(self, name: str) -> None:
        """Проверить наличие заголовка."""
        with allure.step(f'Checking heading "{name}" is visible'):
            expect(self.page.get_by_role("heading", name=name)).to_be_visible()

    def expect_visible(self, locator: Locator, timeout: int = 10000) -> None:
        """Проверить что элемент видим."""
        with allure.step("Checking element is visible"):
            expect(locator).to_be_visible(timeout=timeout)

    def expect_hidden(self, locator: Locator, timeout: int = 10000) -> None:
        """Проверить что элемент скрыт."""
        with allure.step("Checking element is hidden"):
            expect(locator).to_be_hidden(timeout=timeout)
