"""PCO: Компонент уведомлений/тостов (переиспользуемый)."""
import allure
from playwright.sync_api import Page, expect

from tests.components.base_component import BaseComponent


class NotificationComponent(BaseComponent):
    """Универсальный компонент toast-уведомлений."""

    def __init__(self, page: Page):
        super().__init__(page)

    def check_visible_error(self, text: str, timeout: int = 10000) -> None:
        """Проверить что отображается ошибка с указанным текстом."""
        with allure.step(f'Checking error notification "{text}" is visible'):
            expect(self.page.get_by_text(text, exact=True)).to_be_visible(timeout=timeout)
