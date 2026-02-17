"""auth-13: Пароль отображается точками."""
import allure
import pytest
from tests.pages.sign_in_page import SignInPage


@pytest.mark.regression
@pytest.mark.authorization
@allure.epic("Авторизация")
@allure.feature("Вход по телефону")
@allure.story("UI поведение полей")
@allure.tag("Regression", "Authorization", "UI")
class TestAuth13:

    @allure.title("auth-13: Пароль отображается точками")
    @allure.severity(allure.severity_level.MINOR)
    @allure.description(
        "Проверка маскировки пароля при вводе. "
        "Поле пароля должно иметь тип password (отображается точками)."
    )
    def test_auth_13_password_masked(self, sign_in_page: SignInPage):
        sign_in_page.visit("https://app.rizz.market/auth/sign-in")
        sign_in_page.click_other_methods_button()
        sign_in_page.login_form.fill_password(password="89087814701")
        sign_in_page.login_form.check_password_masked()
