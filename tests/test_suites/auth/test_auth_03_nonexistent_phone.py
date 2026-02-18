"""auth-03: Отображение ошибки при авторизации по несуществующему номеру телефона."""
import allure
import pytest

from tests.pages.sign_in_page import SignInPage


@pytest.mark.regression
@pytest.mark.authorization
@allure.epic("Авторизация")
@allure.feature("Вход по телефону")
@allure.story("Невалидные данные")
@allure.tag("Regression", "Authorization")
class TestAuth03:
    """auth-03: Отображение ошибки при авторизации по несуществующему номеру телефона.

    Предусловие:
        телефон: +7 908 781 0000
        Пароль: Gub89087814701
    """

    @allure.title("auth-03: Ошибка при авторизации по несуществующему номеру телефона")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description(
        "Шаги:\n"
        "1) Ввести телефон в поле 'Телефон' данные '+7 908 777 0000'\n"
        "2) Ввести пароль в поле 'Пароль' данные 'паролькин9876'\n"
        "3) Нажать на кнопку 'Войти'\n\n"
        "Ожидаемый результат:\n"
        "1) Отображается ошибка 'Пользователь не найден'\n"
        "2) Пользователь не авторизован"
    )
    def test_auth_03_nonexistent_phone(self, sign_in_page: SignInPage):
        # Предусловие: открыть страницу авторизации и форму
        sign_in_page.visit()
        sign_in_page.click_other_methods_button()

        # 1) Ввести телефон в поле "Телефон" данные "+7 908 777 0000"
        sign_in_page.login_form.fill_phone(phone="9087770000")

        # 2) Ввести пароль в поле "Пароль" данные "паролькин9876"
        sign_in_page.login_form.fill_password(password="паролькин9876")

        # 3) Нажать на кнопку "Войти"
        sign_in_page.click_login_button()

        # ОР 1) Отображается ошибка "Пользователь не найден"
        sign_in_page.check_visible_user_not_found_alert()

        # ОР 2) Пользователь не авторизован — остаётся на sign-in
        sign_in_page.check_visible_sign_in_page()
