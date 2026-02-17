"""auth-01..03: Успешная авторизация."""
import allure
import pytest

from tests.pages.sign_in_page import SignInPage
from tests.pages.campaigns_page import CampaignsPage

PHONE_VALID = "+79087814701"
PASSWORD_VALID = "89087814701"


@pytest.mark.regression
@pytest.mark.authorization
@allure.feature("Авторизация")
@allure.story("Успешная авторизация")
class TestAuthValid:

    @allure.title("auth-01: Авторизация по валидным данным")
    def test_auth_01_valid_login(self, sign_in_page: SignInPage, campaigns_page: CampaignsPage):
        sign_in_page.visit("https://app.rizz.market/auth/sign-in")
        sign_in_page.click_other_methods_button()
        sign_in_page.login_form.fill(phone=PHONE_VALID, password=PASSWORD_VALID)
        sign_in_page.click_login_button()
        campaigns_page.expect_loaded()

    @allure.title("auth-02: Повторная авторизация")
    def test_auth_02_repeat_login(self, sign_in_page: SignInPage, campaigns_page: CampaignsPage):
        sign_in_page.visit("https://app.rizz.market/auth/sign-in")
        sign_in_page.click_other_methods_button()
        sign_in_page.login_form.fill(phone=PHONE_VALID, password=PASSWORD_VALID)
        sign_in_page.click_login_button()
        campaigns_page.expect_loaded()

    @allure.title("auth-03: Сохранение сессии после перезагрузки")
    def test_auth_03_session_persists_after_reload(self, sign_in_page: SignInPage, campaigns_page: CampaignsPage):
        sign_in_page.visit("https://app.rizz.market/auth/sign-in")
        sign_in_page.click_other_methods_button()
        sign_in_page.login_form.fill(phone=PHONE_VALID, password=PASSWORD_VALID)
        sign_in_page.click_login_button()
        campaigns_page.expect_loaded()
        campaigns_page.reload()
        campaigns_page.expect_loaded()
