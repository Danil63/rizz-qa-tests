"""PCO: Компонент отклика на бартер (карточка/модалка)."""
import re

import allure
from playwright.sync_api import Page, Locator, expect

from tests.components.base_component import BaseComponent


class BarterResponseComponent(BaseComponent):
    """Операции отправки/проверки отклика на бартер с fallback по разным UI-состояниям."""

    def __init__(self, page: Page):
        super().__init__(page)

        # Глобальные элементы успеха
        self.success_banner_title = page.get_by_text("Отклик отправлен")
        self.success_banner_text = page.get_by_text("Отклик на бартер отправлен")
        self.cancel_response_button = page.get_by_role("button", name="Отменить отклик").first

    def _scope(self) -> Locator:
        """Контекст поиска кнопок отклика: сначала dialog, затем вся страница."""
        dialog = self.page.locator(
            "div[role='dialog']:has(button:has-text('Выполнить за бартер')), "
            "div[role='dialog']:has(button:has-text('Откликнуться на бартер')), "
            "div[role='dialog']:has-text('Социальная сеть')"
        ).first
        if dialog.count() > 0:
            return dialog
        return self.page.locator("body")

    @allure.step('Prepare barter form (click "Выполнить за бартер" if shown)')
    def prepare_barter_form(self) -> None:
        scope = self._scope()
        execute_btn = scope.get_by_role("button", name="Выполнить за бартер").first
        respond_btn = scope.get_by_role("button", name="Откликнуться на бартер").first

        # В одном сценарии сначала нужно нажать "Выполнить за бартер",
        # в другом форма уже открыта и есть "Откликнуться на бартер".
        if execute_btn.count() > 0 and execute_btn.is_visible(timeout=2000):
            execute_btn.click()
            return

        if respond_btn.count() > 0 and respond_btn.is_visible(timeout=2000):
            return

        raise AssertionError("Не найдены кнопки 'Выполнить за бартер' или 'Откликнуться на бартер'")

    @allure.step('Selecting social network account "{account_name}"')
    def select_social_network(self, account_name: str) -> None:
        scope = self._scope()

        trigger_candidates = [
            scope.get_by_role("button", name=re.compile("Социальная сеть", re.I)).first,
            scope.get_by_role("combobox", name=re.compile("Социальная сеть", re.I)).first,
            scope.locator("input[placeholder*='Социальная сеть'], input[aria-label*='Социальная сеть']").first,
            scope.get_by_text("Социальная сеть", exact=False).first,
        ]

        opened = False
        for trigger in trigger_candidates:
            try:
                if trigger.count() > 0 and trigger.is_visible(timeout=1500):
                    trigger.click()
                    opened = True
                    break
            except Exception:
                continue

        if not opened:
            raise AssertionError("Не удалось открыть dropdown 'Социальная сеть'")

        option_candidates = [
            scope.get_by_role("option", name=account_name).first,
            scope.get_by_role("button", name=account_name).first,
            scope.get_by_text(account_name, exact=False).first,
            self.page.get_by_role("option", name=account_name).first,
            self.page.get_by_text(account_name, exact=False).first,
        ]

        for option in option_candidates:
            try:
                if option.count() > 0 and option.is_visible(timeout=2500):
                    option.click()
                    return
            except Exception:
                continue

        raise AssertionError(f"Не найден аккаунт '{account_name}' в dropdown 'Социальная сеть'")

    @allure.step('Clicking "Откликнуться на бартер"')
    def click_respond_barter(self) -> None:
        scope = self._scope()
        respond_barter_button = scope.get_by_role("button", name="Откликнуться на бартер").first
        expect(respond_barter_button).to_be_visible(timeout=10000)
        respond_barter_button.click()

    @allure.step('Checking success banner "Отклик отправлен" is visible')
    def check_success_banner_visible(self) -> None:
        expect(self.success_banner_title).to_be_visible(timeout=10000)

    @allure.step('Checking text "Отклик на бартер отправлен" is visible')
    def check_success_text_visible(self) -> None:
        expect(self.success_banner_text).to_be_visible()

    @allure.step('Checking "Отменить отклик" button is visible')
    def check_cancel_button_visible(self) -> None:
        expect(self.cancel_response_button).to_be_visible(timeout=10000)
