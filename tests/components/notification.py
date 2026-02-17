"""PCO: Компонент уведомлений/тостов (переиспользуемый)."""
from playwright.sync_api import Page, Locator, expect


class Notification:
    """Универсальный компонент toast-уведомлений."""

    def __init__(self, page: Page):
        self._page = page

    def expect_error(self, text: str, timeout: int = 10000) -> None:
        """Проверить что отображается ошибка с указанным текстом."""
        expect(
            self._page.get_by_text(text, exact=True)
        ).to_be_visible(timeout=timeout)

    def expect_no_error(self, text: str, timeout: int = 3000) -> None:
        """Проверить что ошибка НЕ отображается."""
        expect(
            self._page.get_by_text(text, exact=True)
        ).not_to_be_visible(timeout=timeout)
