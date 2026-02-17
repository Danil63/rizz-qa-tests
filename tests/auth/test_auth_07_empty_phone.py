"""auth-07: Пустой телефон."""
import allure
import pytest
from tests.pages.sign_in_page import SignInPage

@pytest.mark.regression
@pytest.mark.authorization
@allure.feature("Авторизация")
@allure.story("Валидация полей")
class TestAuth07:
    @allure.title("auth-07: Пустой телефон")
    def test_auth_07_empty_phone(self, sign_in_page: SignInPage):
        sign_in_page.visit("https://app.rizz.market/auth/sign-in")
        sign_in_page.click_other_methods_button()
        sign_in_page.login_form.fill_password(password="89087814701")
        sign_in_page.click_login_button()
        sign_in_page.wait()
        sign_in_page.check_visible_sign_in_page()
