"""POM: Страница авторизации (sign-in)."""
from playwright.sync_api import Page, expect

from tests.pages.base_page import BasePage
from tests.components.phone_input import PhoneInput
from tests.components.password_input import PasswordInput
from tests.components.notification import Notification


class SignInPage(BasePage):
    """Page Object для https://app.rizz.market/auth/sign-in."""

    URL = "https://app.rizz.market/auth/sign-in"

    def __init__(self, page: Page):
        super().__init__(page)
        self.phone = PhoneInput(page)
        self.password = PasswordInput(page)
        self.notification = Notification(page)

    # ── Действия ──────────────────────────────────────────────

    def open_phone_form(self) -> "SignInPage":
        """Открыть форму входа по телефону."""
        self.navigate()
        self.page.get_by_role("button", name="Другие способы входа").click()
        self.phone.locator.wait_for(state="visible")
        return self

    def click_login(self) -> None:
        """Нажать кнопку 'Войти'."""
        self.page.get_by_role("button", name="Войти", exact=True).click()

    def click_create_account(self) -> None:
        """Нажать 'Создать аккаунт'."""
        self.page.get_by_role("link", name="Создать аккаунт").click()

    def click_forgot_password(self) -> None:
        """Нажать 'Забыли пароль?'."""
        self.page.get_by_role("link", name="Забыли пароль?").click()

    # ── Проверки ──────────────────────────────────────────────

    def expect_on_sign_in(self) -> None:
        """Проверить что мы на странице входа."""
        self.expect_url_contains(r".*/auth/sign-in")
        self.expect_heading("Вход")

    def expect_error_user_not_found(self) -> None:
        """Проверить ошибку 'Пользователь не найден'."""
        self.notification.expect_error("Пользователь не найден")

    def expect_on_sign_up(self) -> None:
        """Проверить переход на регистрацию."""
        self.expect_url_contains(r".*/auth/sign-up")

    def expect_on_recover_password(self) -> None:
        """Проверить переход на восстановление пароля."""
        self.expect_url_contains(r".*/auth/recover-password")
