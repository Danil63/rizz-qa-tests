"""auth-15: Переход на регистрацию."""
import allure
import pytest
from tests.pages.sign_in_page import SignInPage

@pytest.mark.regression
@pytest.mark.authorization
@allure.feature("Авторизация")
@allure.story("Навигация")
class TestAuth15:
    @allure.title("auth-15: Переход на регистрацию")
    def test_auth_15_navigate_to_registration(self, sign_in_page: SignInPage):
        sign_in_page.visit("https://app.rizz.market/auth/sign-in")
        sign_in_page.click_other_methods_button()
        sign_in_page.click_create_account_link()
        sign_in_page.check_visible_sign_up_page()
