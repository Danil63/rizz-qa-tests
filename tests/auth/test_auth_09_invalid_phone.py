"""auth-09: Невалидный формат телефона."""
import allure
import pytest
from tests.pages.sign_in_page import SignInPage


@pytest.mark.regression
@pytest.mark.authorization
@allure.epic("Авторизация")
@allure.feature("Вход по телефону")
@allure.story("Валидация полей")
@allure.tag("Regression", "Authorization", "Validation")
class TestAuth09:

    @allure.title("auth-09: Невалидный формат телефона")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description(
        "Проверка поведения при вводе телефона в невалидном формате. "
        "Пользователь должен остаться на странице авторизации."
    )
    def test_auth_09_invalid_phone_format(self, sign_in_page: SignInPage):
        sign_in_page.visit("https://app.rizz.market/auth/sign-in")
        sign_in_page.click_other_methods_button()
        sign_in_page.login_form.fill(phone="+77777777777", password="89087814701")
        sign_in_page.click_login_button()
        sign_in_page.wait()
        sign_in_page.check_visible_sign_in_page()
