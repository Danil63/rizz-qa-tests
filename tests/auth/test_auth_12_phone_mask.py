"""auth-12: Маска форматирования телефона."""
import allure
import pytest
from tests.pages.sign_in_page import SignInPage


@pytest.mark.regression
@pytest.mark.authorization
@allure.epic("Авторизация")
@allure.feature("Вход по телефону")
@allure.story("UI поведение полей")
@allure.tag("Regression", "Authorization", "UI")
class TestAuth12:

    @allure.title("auth-12: Маска форматирования телефона")
    @allure.severity(allure.severity_level.MINOR)
    @allure.description(
        "Проверка применения маски форматирования при вводе номера телефона. "
        "После ввода номер должен содержать код страны."
    )
    def test_auth_12_phone_mask(self, sign_in_page: SignInPage):
        sign_in_page.visit("https://app.rizz.market/auth/sign-in")
        sign_in_page.click_other_methods_button()
        sign_in_page.login_form.fill_phone(phone="+79087814701")
        sign_in_page.login_form.check_phone_mask()
