"""auth-06..09: Валидация обязательных полей."""
import allure
import pytest

from tests.pages.sign_in_page import SignInPage

PHONE_VALID = "+79087814701"
PASSWORD_VALID = "89087814701"
PHONE_INVALID = "+77777777777"


@pytest.mark.regression
@pytest.mark.authorization
@allure.feature("Авторизация")
@allure.story("Валидация полей")
class TestAuthFieldValidation:

    @allure.title("auth-06: Пустые обязательные поля")
    def test_auth_06_empty_fields(self, sign_in_page: SignInPage):
        sign_in_page.visit("https://app.rizz.market/auth/sign-in")
        sign_in_page.click_other_methods_button()
        sign_in_page.click_login_button()
        sign_in_page.wait()
        sign_in_page.check_visible_sign_in_page()

    @allure.title("auth-07: Пустой телефон")
    def test_auth_07_empty_phone(self, sign_in_page: SignInPage):
        sign_in_page.visit("https://app.rizz.market/auth/sign-in")
        sign_in_page.click_other_methods_button()
        sign_in_page.login_form.fill_password(password=PASSWORD_VALID)
        sign_in_page.click_login_button()
        sign_in_page.wait()
        sign_in_page.check_visible_sign_in_page()

    @allure.title("auth-08: Пустой пароль")
    def test_auth_08_empty_password(self, sign_in_page: SignInPage):
        sign_in_page.visit("https://app.rizz.market/auth/sign-in")
        sign_in_page.click_other_methods_button()
        sign_in_page.login_form.fill_phone(phone=PHONE_VALID)
        sign_in_page.click_login_button()
        sign_in_page.wait()
        sign_in_page.check_visible_sign_in_page()

    @allure.title("auth-09: Невалидный формат телефона")
    def test_auth_09_invalid_phone_format(self, sign_in_page: SignInPage):
        sign_in_page.visit("https://app.rizz.market/auth/sign-in")
        sign_in_page.click_other_methods_button()
        sign_in_page.login_form.fill(phone=PHONE_INVALID, password=PASSWORD_VALID)
        sign_in_page.click_login_button()
        sign_in_page.wait()
        sign_in_page.check_visible_sign_in_page()
