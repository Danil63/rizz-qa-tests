"""auth-04: Ошибка при незарегистрированном пользователе."""
import allure
import pytest
from tests.pages.sign_in_page import SignInPage


@pytest.mark.regression
@pytest.mark.authorization
@allure.epic("Авторизация")
@allure.feature("Вход по телефону")
@allure.story("Невалидные данные")
@allure.tag("Regression", "Authorization")
class TestAuth04:

    @allure.title("auth-04: Ошибка при незарегистрированном пользователе")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description(
        "Проверка отображения ошибки при попытке входа с незарегистрированным телефоном и паролем. "
        "Должно появиться уведомление 'Пользователь не найден'."
    )
    def test_auth_04_unregistered_user(self, sign_in_page: SignInPage):
        sign_in_page.visit("https://app.rizz.market/auth/sign-in")
        sign_in_page.click_other_methods_button()
        sign_in_page.login_form.fill(phone="+79087770001", password="паролькин9876")
        sign_in_page.click_login_button()
        sign_in_page.check_visible_user_not_found_alert()
        sign_in_page.check_visible_sign_in_page()
