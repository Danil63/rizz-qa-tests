"""auth-14: Автоподстановка +7 при вводе с 8."""
import allure
import pytest
from tests.pages.sign_in_page import SignInPage


@pytest.mark.regression
@pytest.mark.authorization
@allure.epic("Авторизация")
@allure.feature("Вход по телефону")
@allure.story("UI поведение полей")
@allure.tag("Regression", "Authorization", "UI")
class TestAuth14:

    @allure.title("auth-14: Автоподстановка +7 при вводе с 8")
    @allure.severity(allure.severity_level.MINOR)
    @allure.description(
        "Проверка автоматической подстановки префикса +7 при вводе номера, начинающегося с 8. "
        "Маска должна преобразовать 8 в +7."
    )
    def test_auth_14_auto_prefix_7(self, sign_in_page: SignInPage):
        sign_in_page.visit("https://app.rizz.market/auth/sign-in")
        sign_in_page.click_other_methods_button()
        sign_in_page.login_form.fill_phone(phone="89087814701")
        sign_in_page.login_form.check_phone_auto_prefix()
