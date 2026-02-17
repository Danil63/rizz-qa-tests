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
        sign_in_page.open_phone_form()
        sign_in_page.fill_and_clear_fields(PHONE_VALID, PASSWORD_VALID)

    @allure.title("auth-11: Видимость placeholder полей")
    def test_auth_11_placeholder_visible(self, sign_in_page: SignInPage):
        sign_in_page.open_phone_form()
        sign_in_page.login_form.check_visible()

    @allure.title("auth-12: Маска форматирования телефона")
    def test_auth_12_phone_mask(self, sign_in_page: SignInPage):
        sign_in_page.open_phone_form()
        sign_in_page.fill_phone_and_check_mask(PHONE_VALID)

    @allure.title("auth-13: Пароль отображается точками")
    def test_auth_13_password_masked(self, sign_in_page: SignInPage):
        sign_in_page.open_phone_form()
        sign_in_page.fill_password_and_check_masked(PASSWORD_VALID)

    @allure.title("auth-14: Автоподстановка +7 при вводе с 8")
    def test_auth_14_auto_prefix_7(self, sign_in_page: SignInPage):
        sign_in_page.open_phone_form()
        sign_in_page.fill_phone_and_check_auto_prefix("89087814701")
