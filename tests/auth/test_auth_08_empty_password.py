"""auth-08: Пустой пароль."""
import allure
import pytest
from tests.pages.sign_in_page import SignInPage


@pytest.mark.regression
@pytest.mark.authorization
@allure.epic("Авторизация")
@allure.feature("Вход по телефону")
@allure.story("Валидация полей")
@allure.tag("Regression", "Authorization", "Validation")
class TestAuth08:

    @allure.title("auth-08: Пустой пароль")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description(
        "Проверка поведения при нажатии 'Войти' с заполненным телефоном, но пустым паролем. "
        "Пользователь должен остаться на странице авторизации."
    )
    def test_auth_08_empty_password(self, sign_in_page: SignInPage):
        sign_in_page.visit("https://app.rizz.market/auth/sign-in")
        sign_in_page.click_other_methods_button()
        sign_in_page.login_form.fill_phone(phone="+79087814701")
        sign_in_page.click_login_button()
        sign_in_page.wait()
        sign_in_page.check_visible_sign_in_page()
