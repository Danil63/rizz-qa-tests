"""auth-04: Отображение ошибки при игнорировании заполнения обязательных полей."""
import allure
import pytest

from tests.pages.sign_in_page import SignInPage


@pytest.mark.regression
@pytest.mark.authorization
@allure.epic("Авторизация")
@allure.feature("Вход по телефону")
@allure.story("Валидация полей")
@allure.tag("Regression", "Authorization", "Validation")
class TestAuth04:
    """auth-04: Отображение ошибки при игнорировании заполнения обязательных полей."""

    @allure.title("auth-04: Ошибка при игнорировании заполнения обязательных полей")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description(
        "Шаги:\n"
        "1) Нажать на кнопку 'Войти' проигнорировав заполнение обязательных полей\n\n"
        "Ожидаемый результат:\n"
        "1) Названия полей телефон/пароль окрашиваются в красный, под полем отображается ошибка\n"
        "2) Пользователь не авторизован\n"
        "3) Пользователь остается на url: https://app.rizz.market/auth/sign-in"
    )
    def test_auth_04_empty_fields(self, sign_in_page: SignInPage):
        # Предусловие: открыть страницу авторизации и форму
        sign_in_page.visit()
        sign_in_page.click_other_methods_button()

        # 1) Нажать на кнопку "Войти" проигнорировав заполнение обязательных полей
        sign_in_page.click_login_button()

        # ОР 1) Поля подсвечены ошибкой + текст ошибки под полем
        sign_in_page.login_form.check_phone_has_error()
        sign_in_page.login_form.check_phone_error_message("Невалидный номер телефона")

        # ОР 3) Пользователь остается на url: .../auth/sign-in
        sign_in_page.check_visible_sign_in_page()
