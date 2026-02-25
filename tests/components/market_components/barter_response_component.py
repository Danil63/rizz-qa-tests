"""PCO: Компонент отклика на бартер (карточка/модалка)."""
import re

import allure
from playwright.sync_api import Page, Locator, expect

from tests.components.base_component import BaseComponent


class BarterResponseComponent(BaseComponent):
    """Операции отправки/проверки отклика на бартер с fallback по разным UI-состояниям."""

    def __init__(self, page: Page):
        super().__init__(page)

        self.success_banner_title = page.get_by_text("Отклик отправлен")
        self.success_banner_text = page.get_by_text("Отклик на бартер отправлен")
        self.cancel_response_button = page.get_by_role("button", name="Отменить отклик").first

    def _scope(self) -> Locator:
        """Контекст поиска: сначала видимый dialog, затем весь документ."""
        dialogs = self.page.locator("div[role='dialog']")
        for i in range(dialogs.count()):
            d = dialogs.nth(i)
            try:
                if d.is_visible(timeout=300):
                    return d
            except Exception:
                continue
        return self.page.locator("body")

    def _find_barter_action_button(self, scope: Locator) -> Locator:
        """Найти кнопку начала/подтверждения отклика на бартер (варианты текста)."""
        candidates = [
            scope.get_by_role("button", name="Выполнить за бартер").first,
            scope.get_by_role("button", name="Откликнуться на бартер").first,
            scope.get_by_role("button", name=re.compile("бартер", re.I)).first,
            scope.locator("button:has-text('Выполнить за бартер')").first,
            scope.locator("button:has-text('Откликнуться на бартер')").first,
            scope.locator("button:has-text('Откликнуться')").first,
        ]
        for btn in candidates:
            try:
                if btn.count() > 0 and btn.is_visible(timeout=1200):
                    return btn
            except Exception:
                continue
        raise AssertionError("Не найдена кнопка действия по бартеру (Выполнить/Откликнуться)")

    @allure.step('Prepare barter form (click first barter action if required)')
    def prepare_barter_form(self) -> None:
        scope = self._scope()

        # Если поле соцсети уже есть — форма уже раскрыта, клик не нужен
        social_inputs = [
            scope.get_by_role("button", name=re.compile("Социальная сеть", re.I)).first,
            scope.get_by_role("combobox", name=re.compile("Социальная сеть", re.I)).first,
            scope.locator("input[placeholder*='Социальная сеть'], input[aria-label*='Социальная сеть']").first,
            scope.get_by_text("Социальная сеть", exact=False).first,
        ]
        for el in social_inputs:
            try:
                if el.count() > 0 and el.is_visible(timeout=500):
                    return
            except Exception:
                continue

        btn = self._find_barter_action_button(scope)
        btn.click()

    @allure.step('Clicking "Выполнить за бартер" (compat)')
    def click_execute_barter(self) -> None:
        self.prepare_barter_form()

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
        btn_candidates = [
            scope.get_by_role("button", name="Откликнуться на бартер").first,
            scope.get_by_role("button", name=re.compile("Откликнуться", re.I)).first,
            scope.get_by_role("button", name=re.compile("бартер", re.I)).first,
        ]
        for btn in btn_candidates:
            try:
                if btn.count() > 0 and btn.is_visible(timeout=1200):
                    btn.click()
                    return
            except Exception:
                continue
        raise AssertionError("Не найдена кнопка 'Откликнуться на бартер'")

    @allure.step('Checking success banner "Отклик отправлен" is visible')
    def check_success_banner_visible(self) -> None:
        expect(self.success_banner_title).to_be_visible(timeout=10000)

    @allure.step('Checking text "Отклик на бартер отправлен" is visible')
    def check_success_text_visible(self) -> None:
        expect(self.success_banner_text).to_be_visible(timeout=10000)

    @allure.step('Checking "Отменить отклик" button is visible')
    def check_cancel_button_visible(self) -> None:
        expect(self.cancel_response_button).to_be_visible(timeout=10000)
