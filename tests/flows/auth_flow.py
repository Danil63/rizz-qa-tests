"""PFA: Флоу авторизации."""
import allure
from playwright.sync_api import Page

from tests.pages.sign_in_page import SignInPage


class AuthFlow:
    """Page Factory / Flow для авторизации на платформе."""

    def __init__(self, page: Page):
        self.page = page
        self.sign_in = SignInPage(page)

    # ── Методы действий ───────────────────────────────────────

    @allure.step('Login with phone "{phone}"')
    def login_with_phone(self, phone: str, password: str) -> None:
        """Полный флоу логина по телефону."""
        self.sign_in.visit()
        self.sign_in.click_other_methods_button()
        self.sign_in.login_form.fill(phone, password)
        self.sign_in.click_login_button()

    @allure.step('Login expecting error with phone "{phone}"')
    def login_expect_error(self, phone: str, password: str, error_text: str) -> None:
        """Логин с ожиданием ошибки."""
        self.login_with_phone(phone, password)
        self.sign_in.notification.check_visible_error(error_text)

    @allure.step('Submit empty login form')
    def login_empty_submit(self) -> None:
        """Сабмит пустой формы."""
        self.sign_in.visit()
        self.sign_in.click_other_methods_button()
        self.sign_in.click_login_button()

    @allure.step('Submit with phone only "{phone}"')
    def login_phone_only(self, phone: str) -> None:
        """Сабмит только с телефоном."""
        self.sign_in.visit()
        self.sign_in.click_other_methods_button()
        self.sign_in.login_form.fill_phone(phone)
        self.sign_in.click_login_button()

    @allure.step('Submit with password only')
    def login_password_only(self, password: str) -> None:
        """Сабмит только с паролем."""
        self.sign_in.visit()
        self.sign_in.click_other_methods_button()
        self.sign_in.login_form.fill_password(password)
        self.sign_in.click_login_button()
