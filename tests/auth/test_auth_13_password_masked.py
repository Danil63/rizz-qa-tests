"""auth-13: Пароль отображается точками."""
import allure
import pytest
from tests.pages.sign_in_page import SignInPage

@pytest.mark.regression
@pytest.mark.authorization
@allure.feature("Авторизация")
@allure.story("UI поведение полей")
class TestAuth13:
    @allure.title("auth-13: Пароль отображается точками")
    def test_auth_13_password_masked(self, sign_in_page: SignInPage):
        sign_in_page.visit("https://app.rizz.market/auth/sign-in")
        sign_in_page.click_other_methods_button()
        sign_in_page.login_form.fill_password(password="89087814701")
        sign_in_page.login_form.check_password_masked()
