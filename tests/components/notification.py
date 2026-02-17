"""PCO: Компонент уведомлений/тостов (переиспользуемый)."""
from playwright.sync_api import Page, expect

from tests.components.base_component import BaseComponent


class NotificationComponent(BaseComponent):
    def __init__(self, page: Page):
        super().__init__(page)

    def check_visible_error(self, text: str, timeout: int = 10000) -> None:
        expect(self.page.get_by_text(text, exact=True)).to_be_visible(timeout=timeout)
