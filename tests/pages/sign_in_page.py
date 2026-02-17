"""POM: Страница авторизации (sign-in)."""
import re

import allure
from playwright.sync_api import Page, expect

from tests.pages.base_page import BasePage
from tests.components.auth.login_form_component import LoginFormComponent
from tests.components.notification import NotificationComponent


class SignInPage(BasePage):
    """Page Object для https://app.rizz.market/auth/sign-in."""

    URL = "https://app.rizz.market/auth/sign-in"

    def __init__(self, page: Page):
        super().__init__(page)

        # Компоненты
        self.login_form = LoginFormComponent(page)
        self.notification = NotificationComponent(page)

        # Локаторы элементов страницы
        self.other_methods_button = page.get_by_role("button", name="Другие способы входа")
        self.login_button = page.get_by_role("button", name="Войти", exact=True)
        self.create_account_link = page.get_by_role("link", name="Создать аккаунт")
        self.forgot_password_link = page.get_by_role("link", name="Забыли пароль?")

    # ── Методы действий ───────────────────────────────────────

    @allure.step('Opening phone login form')
    def open_phone_form(self) -> "SignInPage":
        """Открыть форму входа по телефону."""
        self.navigate()
        self.other_methods_button.click()
        self.login_form.phone_input.wait_for(state="visible")
        return self

    @allure.step('Clicking "Войти" button')
    def click_login_button(self) -> None:
        """Нажать кнопку 'Войти'."""
        self.login_button.click()

    @allure.step('Clicking "Создать аккаунт" link')
    def click_create_account_link(self) -> None:
        """Нажать 'Создать аккаунт'."""
        self.create_account_link.click()
        self.check_current_url(re.compile(r".*/auth/sign-up"))

    @allure.step('Clicking "Забыли пароль?" link')
    def click_forgot_password_link(self) -> None:
        """Нажать 'Забыли пароль?'."""
        self.forgot_password_link.click()
        self.check_current_url(re.compile(r".*/auth/recover-password"))

    @allure.step('Filling login form and submitting')
    def fill_and_submit(self, phone: str, password: str) -> None:
        """Заполнить форму и нажать Войти."""
        self.login_form.fill(phone, password)
        self.click_login_button()

    @allure.step('Filling phone and checking mask')
    def fill_phone_and_check_mask(self, phone: str) -> None:
        """Ввести телефон и проверить маску."""
        self.login_form.fill_phone(phone)
        self.login_form.check_phone_mask()

    @allure.step('Filling password and checking it is masked')
    def fill_password_and_check_masked(self, password: str) -> None:
        """Ввести пароль и проверить что отображается точками."""
        self.login_form.fill_password(password)
        self.login_form.check_password_masked()

    @allure.step('Filling phone starting with 8 and checking auto-prefix +7')
    def fill_phone_and_check_auto_prefix(self, phone: str) -> None:
        """Ввести телефон с 8 и проверить автоподстановку +7."""
        self.login_form.fill_phone(phone)
        self.login_form.check_phone_auto_prefix()

    @allure.step('Filling form, clearing fields and checking they are empty')
    def fill_and_clear_fields(self, phone: str, password: str) -> None:
        """Заполнить форму, очистить поля и проверить что пустые."""
        self.login_form.fill(phone, password)
        self.login_form.clear_phone()
        self.login_form.clear_password()
        self.login_form.check_empty_phone()
        self.login_form.check_empty_password()

    # ── Методы проверок ───────────────────────────────────────

    @allure.step('Checking sign-in page is displayed')
    def check_visible_sign_in_page(self) -> None:
        """Проверить что мы на странице входа."""
        self.expect_url_contains(r".*/auth/sign-in")
        self.expect_heading("Вход")

    @allure.step('Checking "Пользователь не найден" error is visible')
    def check_visible_user_not_found_alert(self) -> None:
        """Проверить ошибку 'Пользователь не найден'."""
        self.notification.check_visible_error("Пользователь не найден")
