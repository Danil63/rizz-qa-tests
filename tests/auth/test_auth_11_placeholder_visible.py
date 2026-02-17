"""auth-11: Видимость placeholder полей."""
import allure
import pytest
from tests.pages.sign_in_page import SignInPage

@pytest.mark.regression
@pytest.mark.authorization
@allure.feature("Авторизация")
@allure.story("UI поведение полей")
class TestAuth11:
    @allure.title("auth-11: Видимость placeholder полей")
    def test_auth_11_placeholder_visible(self, sign_in_page: SignInPage):
        sign_in_page.visit("https://app.rizz.market/auth/sign-in")
        sign_in_page.click_other_methods_button()
        sign_in_page.login_form.check_visible()
