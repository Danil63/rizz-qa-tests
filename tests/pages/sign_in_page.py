"""POM: Страница авторизации (sign-in)."""
import re

import allure
from playwright.sync_api import Page

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

    @allure.step('Clicking "Другие способы входа" button')
    def click_other_methods_button(self) -> None:
        """Нажать 'Другие способы входа'."""
        self.other_methods_button.click()
        self.login_form.phone_input.wait_for(state="visible")

    @allure.step('Clicking "Войти" button')
    def click_login_button(self) -> None:
        """Нажать кнопку 'Войти'."""
        self.login_button.click()

    @allure.step('Clicking "Создать аккаунт" link')
    def click_create_account_link(self) -> None:
        """Нажать 'Создать аккаунт'."""
        self.create_account_link.click()

    @allure.step('Clicking "Забыли пароль?" link')
    def click_forgot_password_link(self) -> None:
        """Нажать 'Забыли пароль?'."""
        self.forgot_password_link.click()

    # ── Методы проверок ───────────────────────────────────────

    @allure.step('Checking sign-in page is displayed')
    def check_visible_sign_in_page(self) -> None:
        """Проверить что мы на странице входа."""
        self.expect_url_contains(r".*/auth/sign-in")
        self.expect_heading("Вход")

    @allure.step('Checking redirect to sign-up page')
    def check_visible_sign_up_page(self) -> None:
        """Проверить переход на регистрацию."""
        self.expect_url_contains(r".*/auth/sign-up")

    @allure.step('Checking redirect to recover-password page')
    def check_visible_recover_password_page(self) -> None:
        """Проверить переход на восстановление пароля."""
        self.expect_url_contains(r".*/auth/recover-password")

    @allure.step('Checking "Пользователь не найден" error')
    def check_visible_user_not_found_alert(self) -> None:
        """Проверить ошибку 'Пользователь не найден'."""
        self.notification.check_visible_error("Пользователь не найден")
