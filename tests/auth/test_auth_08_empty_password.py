"""auth-08: Пустой пароль."""
import allure
import pytest
from tests.pages.sign_in_page import SignInPage

@pytest.mark.regression
@pytest.mark.authorization
@allure.feature("Авторизация")
@allure.story("Валидация полей")
class TestAuth08:
    @allure.title("auth-08: Пустой пароль")
    def test_auth_08_empty_password(self, sign_in_page: SignInPage):
        sign_in_page.visit("https://app.rizz.market/auth/sign-in")
        sign_in_page.click_other_methods_button()
        sign_in_page.login_form.fill_phone(phone="+79087814701")
        sign_in_page.click_login_button()
        sign_in_page.wait()
        sign_in_page.check_visible_sign_in_page()
