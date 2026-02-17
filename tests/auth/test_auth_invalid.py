"""auth-04..05: Ошибки при невалидных данных."""
import allure
import pytest

from tests.pages.sign_in_page import SignInPage

PHONE_VALID = "+79087814701"
PASSWORD_VALID = "89087814701"
PHONE_UNREGISTERED = "+79087770001"
PASSWORD_UNREGISTERED = "паролькин9876"
PHONE_NONEXISTENT = "+79087810000"


@pytest.mark.regression
@pytest.mark.authorization
@allure.feature("Авторизация")
@allure.story("Невалидные данные")
class TestAuthInvalidCredentials:

    @allure.title("auth-04: Ошибка при незарегистрированном пользователе")
    def test_auth_04_unregistered_user(self, sign_in_page: SignInPage):
        sign_in_page.visit("https://app.rizz.market/auth/sign-in")
        sign_in_page.click_other_methods_button()
        sign_in_page.login_form.fill(phone=PHONE_UNREGISTERED, password=PASSWORD_UNREGISTERED)
        sign_in_page.click_login_button()
        sign_in_page.check_visible_user_not_found_alert()
        sign_in_page.check_visible_sign_in_page()

    @allure.title("auth-05: Ошибка при несуществующем номере")
    def test_auth_05_nonexistent_phone(self, sign_in_page: SignInPage):
        sign_in_page.visit("https://app.rizz.market/auth/sign-in")
        sign_in_page.click_other_methods_button()
        sign_in_page.login_form.fill(phone=PHONE_NONEXISTENT, password=PASSWORD_VALID)
        sign_in_page.click_login_button()
        sign_in_page.check_visible_user_not_found_alert()
        sign_in_page.check_visible_sign_in_page()
