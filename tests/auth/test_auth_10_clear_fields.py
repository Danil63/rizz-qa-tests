"""auth-10: Очистка полей вручную."""
import allure
import pytest
from tests.pages.sign_in_page import SignInPage


@pytest.mark.regression
@pytest.mark.authorization
@allure.epic("Авторизация")
@allure.feature("Вход по телефону")
@allure.story("UI поведение полей")
@allure.tag("Regression", "Authorization", "UI")
class TestAuth10:

    @allure.title("auth-10: Очистка полей вручную")
    @allure.severity(allure.severity_level.MINOR)
    @allure.description(
        "Проверка возможности очистки заполненных полей телефона и пароля. "
        "После очистки оба поля должны быть пустыми."
    )
    def test_auth_10_clear_fields(self, sign_in_page: SignInPage):
        sign_in_page.visit("https://app.rizz.market/auth/sign-in")
        sign_in_page.click_other_methods_button()
        sign_in_page.login_form.fill(phone="+79087814701", password="89087814701")
        sign_in_page.login_form.clear_phone()
        sign_in_page.login_form.clear_password()
        sign_in_page.login_form.check_empty_phone()
        sign_in_page.login_form.check_empty_password()
