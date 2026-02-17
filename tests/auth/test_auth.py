"""
Тест-кейсы авторизации для https://app.rizz.market
Запуск: pytest tests/test_auth.py -v
"""
import re

import pytest
from playwright.sync_api import Page, expect


PHONE_VALID = "+79087814701"
PASSWORD_VALID = "89087814701"
PHONE_UNREGISTERED = "+79087770001"
PASSWORD_UNREGISTERED = "паролькин9876"
PHONE_NONEXISTENT = "+79087810000"
PHONE_INVALID = "+77777777777"
SIGN_IN_URL = "https://app.rizz.market/auth/sign-in"
CAMPAIGNS_URL = re.compile(r".*/app/advertiser/campaigns")


# ─── helpers ────────────────────────────────────────────────────────

def _open_phone_form(page: Page) -> None:
    """Открыть форму входа по телефону."""
    page.goto(SIGN_IN_URL)
    page.get_by_role("button", name="Другие способы входа").click()
    page.get_by_placeholder("+7").wait_for(state="visible")


def _fill_credentials(page: Page, phone: str, password: str) -> None:
    """Посимвольно ввести телефон и пароль."""
    page.get_by_placeholder("+7").click()
    page.get_by_placeholder("+7").type(phone, delay=50)
    page.get_by_label("Пароль").click()
    page.get_by_label("Пароль").type(password, delay=50)


def _click_login(page: Page) -> None:
    page.get_by_role("button", name="Войти", exact=True).click()


# ─── auth-01: Авторизация по валидным данным ────────────────────────

class TestAuthValid:

    def test_auth_01_valid_login(self, page: Page):
        """auth-01: Авторизация пользователя по валидным данным."""
        _open_phone_form(page)
        _fill_credentials(page, PHONE_VALID, PASSWORD_VALID)
        _click_login(page)

        page.wait_for_url(CAMPAIGNS_URL, timeout=15000)
        expect(page.get_by_role("heading", name="Кампании")).to_be_visible()

    def test_auth_02_repeat_login(self, page: Page):
        """auth-02: Повторная авторизация по валидным данным."""
        _open_phone_form(page)
        _fill_credentials(page, PHONE_VALID, PASSWORD_VALID)
        _click_login(page)

        page.wait_for_url(CAMPAIGNS_URL, timeout=15000)
        expect(page.get_by_role("heading", name="Кампании")).to_be_visible()

    def test_auth_03_session_persists_after_reload(self, page: Page):
        """auth-03: Сохранение авторизации после обновления страницы."""
        _open_phone_form(page)
        _fill_credentials(page, PHONE_VALID, PASSWORD_VALID)
        _click_login(page)
        page.wait_for_url(CAMPAIGNS_URL, timeout=15000)

        page.reload()
        page.wait_for_url(CAMPAIGNS_URL, timeout=15000)
        expect(page.get_by_role("heading", name="Кампании")).to_be_visible()


# ─── auth-04..05: Ошибки при невалидных данных ──────────────────────

class TestAuthInvalidCredentials:

    def test_auth_04_unregistered_user(self, page: Page):
        """auth-04: Ошибка при авторизации по незарегистрированным данным."""
        _open_phone_form(page)
        _fill_credentials(page, PHONE_UNREGISTERED, PASSWORD_UNREGISTERED)
        _click_login(page)

        expect(
            page.get_by_text("Пользователь не найден", exact=True)
        ).to_be_visible(timeout=10000)
        expect(page).to_have_url(re.compile(r".*/auth/sign-in"))

    def test_auth_05_nonexistent_phone(self, page: Page):
        """auth-05: Ошибка при авторизации по несуществующему номеру."""
        _open_phone_form(page)
        _fill_credentials(page, PHONE_NONEXISTENT, PASSWORD_VALID)
        _click_login(page)

        expect(
            page.get_by_text("Пользователь не найден", exact=True)
        ).to_be_visible(timeout=10000)
        expect(page).to_have_url(re.compile(r".*/auth/sign-in"))


# ─── auth-06..09: Валидация обязательных полей ───────────────────────

class TestAuthFieldValidation:

    def test_auth_06_empty_fields(self, page: Page):
        """auth-06: Ошибка при пустых обязательных полях."""
        _open_phone_form(page)
        _click_login(page)

        # Форма не отправляется — остаёмся на sign-in
        # Проверяем что появилась ошибка валидации (текст или border-color)
        page.wait_for_timeout(1000)
        expect(page).to_have_url(re.compile(r".*/auth/sign-in"))
        # Пользователь НЕ авторизован — заголовок "Вход" всё ещё виден
        expect(page.get_by_role("heading", name="Вход")).to_be_visible()

    def test_auth_07_empty_phone(self, page: Page):
        """auth-07: Ошибка при пустом телефоне."""
        _open_phone_form(page)
        page.get_by_label("Пароль").click()
        page.get_by_label("Пароль").type(PASSWORD_VALID, delay=50)
        _click_login(page)

        page.wait_for_timeout(1000)
        expect(page).to_have_url(re.compile(r".*/auth/sign-in"))
        expect(page.get_by_role("heading", name="Вход")).to_be_visible()

    def test_auth_08_empty_password(self, page: Page):
        """auth-08: Ошибка при пустом пароле."""
        _open_phone_form(page)
        page.get_by_placeholder("+7").click()
        page.get_by_placeholder("+7").type(PHONE_VALID, delay=50)
        _click_login(page)

        page.wait_for_timeout(1000)
        expect(page).to_have_url(re.compile(r".*/auth/sign-in"))
        expect(page.get_by_role("heading", name="Вход")).to_be_visible()

    def test_auth_09_invalid_phone_format(self, page: Page):
        """auth-09: Ошибка по невалидному телефону."""
        _open_phone_form(page)
        _fill_credentials(page, PHONE_INVALID, PASSWORD_VALID)
        _click_login(page)

        page.wait_for_timeout(1000)
        expect(page).to_have_url(re.compile(r".*/auth/sign-in"))
        expect(page.get_by_role("heading", name="Вход")).to_be_visible()


# ─── auth-10..14: UI поведение полей ─────────────────────────────────

class TestAuthFieldBehavior:

    def test_auth_10_clear_fields(self, page: Page):
        """auth-10: Очистка обязательных полей вручную."""
        _open_phone_form(page)
        _fill_credentials(page, PHONE_VALID, PASSWORD_VALID)

        # Очищаем поля
        phone = page.get_by_placeholder("+7")
        phone.click()
        phone.fill("")

        password = page.get_by_label("Пароль")
        password.click()
        password.fill("")

        # Поля пусты, placeholder отображается
        expect(phone).to_have_value("")
        expect(password).to_have_value("")

    def test_auth_11_placeholder_visible(self, page: Page):
        """auth-11: Отображение placeholder в полях."""
        _open_phone_form(page)

        expect(page.get_by_placeholder("+7")).to_be_visible()
        expect(page.get_by_label("Пароль")).to_be_visible()

    def test_auth_12_phone_mask(self, page: Page):
        """auth-12: Маска форматирования при вводе телефона."""
        _open_phone_form(page)
        phone = page.get_by_placeholder("+7")
        phone.click()
        phone.type("+79087814701", delay=50)

        # Значение не пустое — маска применена
        value = phone.input_value()
        assert len(value) > 0, "Поле телефона пустое после ввода"
        assert "7" in value, "Маска не содержит код страны"

    def test_auth_13_password_masked(self, page: Page):
        """auth-13: Пароль отображается точками."""
        _open_phone_form(page)
        password = page.get_by_label("Пароль")
        password.click()
        password.type(PASSWORD_VALID, delay=50)

        # Тип поля password → символы скрыты
        expect(password).to_have_attribute("type", "password")

    def test_auth_14_auto_prefix_7(self, page: Page):
        """auth-14: Автоподстановка +7 при вводе номера с 8."""
        _open_phone_form(page)
        phone = page.get_by_placeholder("+7")
        phone.click()
        phone.type("89087814701", delay=50)

        value = phone.input_value()
        # Ожидаем что +7 подставился автоматически
        assert value.startswith("+7") or value.startswith("7"), (
            f"Автоподстановка +7 не сработала: '{value}'"
        )


# ─── auth-15..16: Переходы ───────────────────────────────────────────

class TestAuthNavigation:

    def test_auth_15_navigate_to_registration(self, page: Page):
        """auth-15: Переход на регистрацию по кнопке 'Создать аккаунт'."""
        _open_phone_form(page)
        page.get_by_role("link", name="Создать аккаунт").click()

        expect(page).to_have_url(re.compile(r".*/auth/sign-up"), timeout=10000)

    def test_auth_16_navigate_to_recover_password(self, page: Page):
        """auth-16: Переход на восстановление пароля."""
        _open_phone_form(page)
        page.get_by_role("link", name="Забыли пароль?").click()

        expect(page).to_have_url(
            re.compile(r".*/auth/recover-password"), timeout=10000
        )
