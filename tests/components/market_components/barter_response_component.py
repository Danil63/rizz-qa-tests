"""PCO: Компонент модалки отклика на бартер."""
import re

import allure
from playwright.sync_api import Page, expect

from tests.components.base_component import BaseComponent


class BarterResponseComponent(BaseComponent):
    """Модалка отклика на бартер — выбор соцсети, подтверждение, баннер успеха."""

    def __init__(self, page: Page):
        super().__init__(page)

        # ── Кнопка «Выполнить за бартер» ──────────────────────
        self.execute_barter_button = page.get_by_role("button", name="Выполнить за бартер")

        # ── Кнопка «Откликнуться на бартер» ───────────────────
        self.respond_barter_button = page.get_by_role("button", name="Откликнуться на бартер")

        # ── Баннер успеха ─────────────────────────────────────
        self.success_banner_title = page.get_by_text("Отклик отправлен")
        self.success_banner_text = page.get_by_text("Отклик на бартер отправлен")
        self.cancel_response_button = page.get_by_role("button", name="Отменить отклик")

    # ── Действия ──────────────────────────────────────────────

    @allure.step('Clicking "Выполнить за бартер"')
    def click_execute_barter(self) -> None:
        expect(self.execute_barter_button).to_be_visible(timeout=15000)
        self.execute_barter_button.click()

    @allure.step('Selecting social network account "{account_name}"')
    def select_social_network(self, account_name: str) -> None:
        # Модалка может рендерить селектор как button/combobox/input.
        # Сначала ждём появления кнопки подтверждения внутри модалки.
        expect(self.respond_barter_button).to_be_visible(timeout=15000)

        trigger_candidates = [
            self.page.get_by_role("button", name=re.compile("Социальная сеть", re.I)).first,
            self.page.get_by_role("combobox", name=re.compile("Социальная сеть", re.I)).first,
            self.page.locator("input[placeholder*='Социальная сеть'], input[aria-label*='Социальная сеть']").first,
            self.page.get_by_text("Социальная сеть", exact=False).first,
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
            raise AssertionError("Не удалось открыть dropdown 'Социальная сеть' в модалке отклика")

        # Варианты элементов списка
        option_candidates = [
            self.page.get_by_role("option", name=account_name).first,
            self.page.get_by_role("button", name=account_name).first,
            self.page.get_by_text(account_name, exact=False).first,
        ]

        for option in option_candidates:
            try:
                if option.count() > 0 and option.is_visible(timeout=3000):
                    option.click()
                    return
            except Exception:
                continue

        raise AssertionError(f"Не найден аккаунт '{account_name}' в dropdown 'Социальная сеть'")

    @allure.step('Clicking "Откликнуться на бартер"')
    def click_respond_barter(self) -> None:
        expect(self.respond_barter_button).to_be_visible(timeout=10000)
        self.respond_barter_button.click()

    # ── Проверки ──────────────────────────────────────────────

    @allure.step('Checking success banner "Отклик отправлен" is visible')
    def check_success_banner_visible(self) -> None:
        expect(self.success_banner_title).to_be_visible(timeout=10000)

    @allure.step('Checking text "Отклик на бартер отправлен" is visible')
    def check_success_text_visible(self) -> None:
        expect(self.success_banner_text).to_be_visible()

    @allure.step('Checking "Отменить отклик" button is visible')
    def check_cancel_button_visible(self) -> None:
        expect(self.cancel_response_button).to_be_visible()
