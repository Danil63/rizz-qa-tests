"""auth-07: Пустой телефон."""
import allure
import pytest
from tests.pages.sign_in_page import SignInPage


@pytest.mark.regression
@pytest.mark.authorization
@allure.epic("Авторизация")
@allure.feature("Вход по телефону")
@allure.story("Валидация полей")
@allure.tag("Regression", "Authorization", "Validation")
class TestAuth07:

    @allure.title("auth-07: Пустой телефон")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description(
        "Проверка поведения при нажатии 'Войти' с заполненным паролем, но пустым телефоном. "
        "Пользователь должен остаться на странице авторизации."
    )
    def test_auth_07_empty_phone(self, sign_in_page: SignInPage):
        sign_in_page.visit("https://app.rizz.market/auth/sign-in")
        sign_in_page.click_other_methods_button()
        sign_in_page.login_form.fill_password(password="89087814701")
        sign_in_page.click_login_button()
        sign_in_page.wait()
        sign_in_page.check_visible_sign_in_page()
