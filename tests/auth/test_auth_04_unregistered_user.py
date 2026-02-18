"""auth-04: Отображение ошибки при авторизации по не зарегистрированным данным."""
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
    """auth-04: Отображение ошибки при авторизации по не зарегистрированным данным.

    Предусловие:
        телефон: +7 908 777 0001
        Пароль: паролькин9876
    """

    @allure.title("auth-04: Ошибка при авторизации по не зарегистрированным данным")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description(
        "Шаги:\n"
        "1) Ввести телефон в поле 'Телефон' данные '+7 908 777 0001'\n"
        "2) Ввести пароль в поле 'Пароль' данные 'паролькин9876'\n"
        "3) Нажать на кнопку 'Войти'\n\n"
        "Ожидаемый результат:\n"
        "1) Отображается ошибка 'Неверный пароль или пользователь не найден'\n"
        "2) Пользователь не авторизован\n"
        "3) Пользователь остается на url: https://app.rizz.market/auth/sign-in"
    )
    def test_auth_04_unregistered_user(self, sign_in_page: SignInPage):
        # Предусловие: открыть страницу авторизации и форму
        sign_in_page.visit()
        sign_in_page.click_other_methods_button()

        # 1) Ввести телефон в поле "Телефон" данные "+7 908 777 0001"
        sign_in_page.login_form.fill_phone(phone="9087770001")

        # 2) Ввести пароль в поле "Пароль" данные "паролькин9876"
        sign_in_page.login_form.fill_password(password="паролькин9876")

        # 3) Нажать на кнопку "Войти"
        sign_in_page.click_login_button()

        # ОР 1) Отображается ошибка "Неверный пароль или пользователь не найден"
        sign_in_page.check_visible_wrong_password_or_user_not_found_alert()

        # ОР 3) Пользователь остается на url: .../auth/sign-in
        sign_in_page.check_visible_sign_in_page()
