"""Базовый класс для всех компонентов (PageComponent)."""
import re
from typing import Pattern

from playwright.sync_api import Page, expect


class BaseComponent:
    """BaseComponent — наследуется всеми компонентами."""

    def __init__(self, page: Page):
        self.page = page

    def check_current_url(self, expected_url: Pattern[str]) -> None:
        """Проверить что текущий URL соответствует паттерну."""
        expect(self.page).to_have_url(expected_url)
