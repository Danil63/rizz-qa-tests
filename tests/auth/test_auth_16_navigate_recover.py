"""auth-16: Переход на восстановление пароля."""
import allure
import pytest
from tests.pages.sign_in_page import SignInPage

@pytest.mark.regression
@pytest.mark.authorization
@allure.feature("Авторизация")
@allure.story("Навигация")
class TestAuth16:
    @allure.title("auth-16: Переход на восстановление пароля")
    def test_auth_16_navigate_to_recover_password(self, sign_in_page: SignInPage):
        sign_in_page.visit("https://app.rizz.market/auth/sign-in")
        sign_in_page.click_other_methods_button()
        sign_in_page.click_forgot_password_link()
        sign_in_page.check_visible_recover_password_page()
