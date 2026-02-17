"""auth-10..14: UI поведение полей."""
import allure
import pytest

from tests.pages.sign_in_page import SignInPage

PHONE_VALID = "+79087814701"
PASSWORD_VALID = "89087814701"


@pytest.mark.regression
@pytest.mark.authorization
@allure.feature("Авторизация")
@allure.story("UI поведение полей")
class TestAuthFieldBehavior:

    @allure.title("auth-10: Очистка полей вручную")
    def test_auth_10_clear_fields(self, sign_in_page: SignInPage):
        sign_in_page.visit("https://app.rizz.market/auth/sign-in")
        sign_in_page.click_other_methods_button()
        sign_in_page.login_form.fill(phone=PHONE_VALID, password=PASSWORD_VALID)
        sign_in_page.login_form.clear_phone()
        sign_in_page.login_form.clear_password()
        sign_in_page.login_form.check_empty_phone()
        sign_in_page.login_form.check_empty_password()

    @allure.title("auth-11: Видимость placeholder полей")
    def test_auth_11_placeholder_visible(self, sign_in_page: SignInPage):
        sign_in_page.visit("https://app.rizz.market/auth/sign-in")
        sign_in_page.click_other_methods_button()
        sign_in_page.login_form.check_visible()

    @allure.title("auth-12: Маска форматирования телефона")
    def test_auth_12_phone_mask(self, sign_in_page: SignInPage):
        sign_in_page.visit("https://app.rizz.market/auth/sign-in")
        sign_in_page.click_other_methods_button()
        sign_in_page.login_form.fill_phone(phone=PHONE_VALID)
        sign_in_page.login_form.check_phone_mask()

    @allure.title("auth-13: Пароль отображается точками")
    def test_auth_13_password_masked(self, sign_in_page: SignInPage):
        sign_in_page.visit("https://app.rizz.market/auth/sign-in")
        sign_in_page.click_other_methods_button()
        sign_in_page.login_form.fill_password(password=PASSWORD_VALID)
        sign_in_page.login_form.check_password_masked()

    @allure.title("auth-14: Автоподстановка +7 при вводе с 8")
    def test_auth_14_auto_prefix_7(self, sign_in_page: SignInPage):
        sign_in_page.visit("https://app.rizz.market/auth/sign-in")
        sign_in_page.click_other_methods_button()
        sign_in_page.login_form.fill_phone(phone="89087814701")
        sign_in_page.login_form.check_phone_auto_prefix()
