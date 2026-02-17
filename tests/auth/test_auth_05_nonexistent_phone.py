"""auth-05: Ошибка при несуществующем номере."""
import allure
import pytest
from tests.pages.sign_in_page import SignInPage


@pytest.mark.regression
@pytest.mark.authorization
@allure.epic("Авторизация")
@allure.feature("Вход по телефону")
@allure.story("Невалидные данные")
@allure.tag("Regression", "Authorization")
class TestAuth05:

    @allure.title("auth-05: Ошибка при несуществующем номере")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description(
        "Проверка ошибки при входе с несуществующим номером телефона, но валидным паролем. "
        "Должно появиться уведомление 'Пользователь не найден'."
    )
    def test_auth_05_nonexistent_phone(self, sign_in_page: SignInPage):
        sign_in_page.visit("https://app.rizz.market/auth/sign-in")
        sign_in_page.click_other_methods_button()
        sign_in_page.login_form.fill(phone="+79087810000", password="89087814701")
        sign_in_page.click_login_button()
        sign_in_page.check_visible_user_not_found_alert()
        sign_in_page.check_visible_sign_in_page()
