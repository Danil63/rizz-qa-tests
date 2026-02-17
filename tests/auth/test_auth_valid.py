"""auth-01..03: Успешная авторизация."""
import allure
import pytest

from tests.flows.auth_flow import AuthFlow

PHONE_VALID = "+79087814701"
PASSWORD_VALID = "89087814701"


@pytest.mark.regression
@pytest.mark.authorization
@allure.feature("Авторизация")
@allure.story("Успешная авторизация")
class TestAuthValid:

    @allure.title("auth-01: Авторизация по валидным данным")
    def test_auth_01_valid_login(self, auth_flow: AuthFlow):
        campaigns = auth_flow.login_with_phone(PHONE_VALID, PASSWORD_VALID)
        campaigns.expect_loaded()

    @allure.title("auth-02: Повторная авторизация")
    def test_auth_02_repeat_login(self, auth_flow: AuthFlow):
        campaigns = auth_flow.login_with_phone(PHONE_VALID, PASSWORD_VALID)
        campaigns.expect_loaded()

    @allure.title("auth-03: Сохранение сессии после перезагрузки")
    def test_auth_03_session_persists_after_reload(self, auth_flow: AuthFlow):
        campaigns = auth_flow.login_with_phone(PHONE_VALID, PASSWORD_VALID)
        campaigns.expect_loaded()
        campaigns.reload()
        campaigns.expect_loaded()
