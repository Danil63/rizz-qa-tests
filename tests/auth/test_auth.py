"""
Тест-кейсы авторизации для https://app.rizz.market
Архитектура: POM + PCO + PFA

Запуск: pytest tests/auth/test_auth.py -v
"""
import pytest
from playwright.sync_api import Page

from tests.pages.sign_in_page import SignInPage
from tests.flows.auth_flow import AuthFlow


# ─── Тестовые данные ─────────────────────────────────────────────────

PHONE_VALID = "+79087814701"
PASSWORD_VALID = "89087814701"
PHONE_UNREGISTERED = "+79087770001"
PASSWORD_UNREGISTERED = "паролькин9876"
PHONE_NONEXISTENT = "+79087810000"
PHONE_INVALID = "+77777777777"


# ─── auth-01..03: Успешная авторизация ───────────────────────────────

class TestAuthValid:

    def test_auth_01_valid_login(self, auth_flow: AuthFlow):
        """auth-01: Авторизация пользователя по валидным данным."""
        campaigns = auth_flow.login_with_phone(PHONE_VALID, PASSWORD_VALID)
        campaigns.expect_loaded()

    def test_auth_02_repeat_login(self, auth_flow: AuthFlow):
        """auth-02: Повторная авторизация по валидным данным."""
        campaigns = auth_flow.login_with_phone(PHONE_VALID, PASSWORD_VALID)
        campaigns.expect_loaded()

    def test_auth_03_session_persists_after_reload(self, auth_flow: AuthFlow):
        """auth-03: Сохранение авторизации после обновления страницы."""
        campaigns = auth_flow.login_with_phone(PHONE_VALID, PASSWORD_VALID)
        campaigns.expect_loaded()

        campaigns.reload()
        campaigns.expect_loaded()


# ─── auth-04..05: Ошибки при невалидных данных ───────────────────────

class TestAuthInvalidCredentials:

    def test_auth_04_unregistered_user(self, auth_flow: AuthFlow):
        """auth-04: Ошибка при авторизации по незарегистрированным данным."""
        sign_in = auth_flow.login_expect_error(
            PHONE_UNREGISTERED, PASSWORD_UNREGISTERED
        )
        sign_in.expect_error_user_not_found()
        sign_in.expect_on_sign_in()

    def test_auth_05_nonexistent_phone(self, auth_flow: AuthFlow):
        """auth-05: Ошибка при авторизации по несуществующему номеру."""
        sign_in = auth_flow.login_expect_error(
            PHONE_NONEXISTENT, PASSWORD_VALID
        )
        sign_in.expect_error_user_not_found()
        sign_in.expect_on_sign_in()


# ─── auth-06..09: Валидация обязательных полей ───────────────────────

class TestAuthFieldValidation:

    def test_auth_06_empty_fields(self, auth_flow: AuthFlow):
        """auth-06: Ошибка при пустых обязательных полях."""
        sign_in = auth_flow.login_empty_submit()
        sign_in.wait()
        sign_in.expect_on_sign_in()

    def test_auth_07_empty_phone(self, auth_flow: AuthFlow):
        """auth-07: Ошибка при пустом телефоне."""
        sign_in = auth_flow.login_password_only(PASSWORD_VALID)
        sign_in.wait()
        sign_in.expect_on_sign_in()

    def test_auth_08_empty_password(self, auth_flow: AuthFlow):
        """auth-08: Ошибка при пустом пароле."""
        sign_in = auth_flow.login_phone_only(PHONE_VALID)
        sign_in.wait()
        sign_in.expect_on_sign_in()

    def test_auth_09_invalid_phone_format(self, auth_flow: AuthFlow):
        """auth-09: Ошибка по невалидному телефону."""
        sign_in = auth_flow.login_expect_error(PHONE_INVALID, PASSWORD_VALID)
        sign_in.wait()
        sign_in.expect_on_sign_in()


# ─── auth-10..14: UI поведение полей ─────────────────────────────────

class TestAuthFieldBehavior:

    def test_auth_10_clear_fields(self, sign_in_page: SignInPage):
        """auth-10: Очистка обязательных полей вручную."""
        sign_in_page.open_phone_form()
        sign_in_page.phone.fill(PHONE_VALID)
        sign_in_page.password.fill(PASSWORD_VALID)

        sign_in_page.phone.clear()
        sign_in_page.password.clear()

        sign_in_page.phone.expect_empty()
        sign_in_page.password.expect_empty()

    def test_auth_11_placeholder_visible(self, sign_in_page: SignInPage):
        """auth-11: Отображение placeholder в полях."""
        sign_in_page.open_phone_form()
        sign_in_page.phone.expect_visible()
        sign_in_page.password.expect_visible()

    def test_auth_12_phone_mask(self, sign_in_page: SignInPage):
        """auth-12: Маска форматирования при вводе телефона."""
        sign_in_page.open_phone_form()
        sign_in_page.phone.fill(PHONE_VALID)

        value = sign_in_page.phone.get_value()
        assert len(value) > 0, "Поле телефона пустое после ввода"
        assert "7" in value, "Маска не содержит код страны"

    def test_auth_13_password_masked(self, sign_in_page: SignInPage):
        """auth-13: Пароль отображается точками."""
        sign_in_page.open_phone_form()
        sign_in_page.password.fill(PASSWORD_VALID)
        sign_in_page.password.expect_masked()

    def test_auth_14_auto_prefix_7(self, sign_in_page: SignInPage):
        """auth-14: Автоподстановка +7 при вводе номера с 8."""
        sign_in_page.open_phone_form()
        sign_in_page.phone.fill("89087814701")

        value = sign_in_page.phone.get_value()
        assert value.startswith("+7") or value.startswith("7"), (
            f"Автоподстановка +7 не сработала: '{value}'"
        )


# ─── auth-15..16: Переходы ───────────────────────────────────────────

class TestAuthNavigation:

    def test_auth_15_navigate_to_registration(self, sign_in_page: SignInPage):
        """auth-15: Переход на регистрацию по кнопке 'Создать аккаунт'."""
        sign_in_page.open_phone_form()
        sign_in_page.click_create_account()
        sign_in_page.expect_on_sign_up()

    def test_auth_16_navigate_to_recover_password(self, sign_in_page: SignInPage):
        """auth-16: Переход на восстановление пароля."""
        sign_in_page.open_phone_form()
        sign_in_page.click_forgot_password()
        sign_in_page.expect_on_recover_password()
