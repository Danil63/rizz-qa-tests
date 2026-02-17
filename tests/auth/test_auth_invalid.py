"""auth-04..05: Ошибки при невалидных данных."""
import allure
import pytest

from tests.flows.auth_flow import AuthFlow

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
    def test_auth_04_unregistered_user(self, auth_flow: AuthFlow):
        sign_in = auth_flow.login_expect_error(PHONE_UNREGISTERED, PASSWORD_UNREGISTERED)
        sign_in.check_visible_user_not_found_alert()
        sign_in.check_visible_sign_in_page()

    @allure.title("auth-05: Ошибка при несуществующем номере")
    def test_auth_05_nonexistent_phone(self, auth_flow: AuthFlow):
        sign_in = auth_flow.login_expect_error(PHONE_NONEXISTENT, PASSWORD_VALID)
        sign_in.check_visible_user_not_found_alert()
        sign_in.check_visible_sign_in_page()
