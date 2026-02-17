"""Базовый класс для всех компонентов (PageComponent)."""
from typing import Pattern

import allure
from playwright.sync_api import Page, expect


class BaseComponent:
    """BaseComponent — наследуется всеми компонентами."""

    def __init__(self, page: Page):
        self.page = page

    def check_current_url(self, expected_url: Pattern[str]) -> None:
        """Проверить что текущий URL соответствует паттерну."""
        with allure.step(f'Checking URL matches pattern'):
            expect(self.page).to_have_url(expected_url)
