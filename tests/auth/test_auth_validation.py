"""auth-06..09: Валидация обязательных полей."""
import allure
import pytest

from tests.flows.auth_flow import AuthFlow

PHONE_VALID = "+79087814701"
PASSWORD_VALID = "89087814701"
PHONE_INVALID = "+77777777777"


@pytest.mark.regression
@pytest.mark.authorization
@allure.feature("Авторизация")
@allure.story("Валидация полей")
class TestAuthFieldValidation:

    @allure.title("auth-06: Пустые обязательные поля")
    def test_auth_06_empty_fields(self, auth_flow: AuthFlow):
        sign_in = auth_flow.login_empty_submit()
        sign_in.wait()
        sign_in.check_visible_sign_in_page()

    @allure.title("auth-07: Пустой телефон")
    def test_auth_07_empty_phone(self, auth_flow: AuthFlow):
        sign_in = auth_flow.login_password_only(PASSWORD_VALID)
        sign_in.wait()
        sign_in.check_visible_sign_in_page()

    @allure.title("auth-08: Пустой пароль")
    def test_auth_08_empty_password(self, auth_flow: AuthFlow):
        sign_in = auth_flow.login_phone_only(PHONE_VALID)
        sign_in.wait()
        sign_in.check_visible_sign_in_page()

    @allure.title("auth-09: Невалидный формат телефона")
    def test_auth_09_invalid_phone_format(self, auth_flow: AuthFlow):
        sign_in = auth_flow.login_expect_error(PHONE_INVALID, PASSWORD_VALID)
        sign_in.wait()
        sign_in.check_visible_sign_in_page()
