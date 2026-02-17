"""auth-12: Маска форматирования телефона."""
import allure
import pytest
from tests.pages.sign_in_page import SignInPage

@pytest.mark.regression
@pytest.mark.authorization
@allure.feature("Авторизация")
@allure.story("UI поведение полей")
class TestAuth12:
    @allure.title("auth-12: Маска форматирования телефона")
    def test_auth_12_phone_mask(self, sign_in_page: SignInPage):
        sign_in_page.visit("https://app.rizz.market/auth/sign-in")
        sign_in_page.click_other_methods_button()
        sign_in_page.login_form.fill_phone(phone="+79087814701")
        sign_in_page.login_form.check_phone_mask()
