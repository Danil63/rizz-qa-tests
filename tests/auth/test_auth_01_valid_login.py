"""auth-01: Авторизация по валидным данным."""
import allure
import pytest
from tests.pages.sign_in_page import SignInPage
from tests.pages.campaigns_page import CampaignsPage


@pytest.mark.regression
@pytest.mark.authorization
@allure.epic("Авторизация")
@allure.feature("Вход по телефону")
@allure.story("Успешная авторизация")
@allure.tag("Regression", "Authorization")
class TestAuth01:

    @allure.title("auth-01: Авторизация по валидным данным")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description(
        "Проверка успешного входа с валидным телефоном и паролем. "
        "После авторизации пользователь должен попасть на страницу кампаний."
    )
    def test_auth_01_valid_login(self, sign_in_page: SignInPage, campaigns_page: CampaignsPage):
        sign_in_page.visit("https://app.rizz.market/auth/sign-in")
        sign_in_page.click_other_methods_button()
        sign_in_page.login_form.fill(phone="+79087814701", password="89087814701")
        sign_in_page.click_login_button()
        campaigns_page.expect_loaded()
