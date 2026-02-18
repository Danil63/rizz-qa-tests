"""auth-06: Отображение ошибки по невалидному телефону."""
import allure
import pytest

from tests.pages.sign_in_page import SignInPage


@pytest.mark.regression
@pytest.mark.authorization
@allure.epic("Авторизация")
@allure.feature("Вход по телефону")
@allure.story("Валидация полей")
@allure.tag("Regression", "Authorization", "Validation")
class TestAuth06:
    """auth-06: Отображение ошибки по невалидному телефону.

    Предусловие:
        телефон: +7 908 777
        Пароль: Gub89087814701
    """

    @allure.title("auth-06: Ошибка по невалидному телефону")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description(
        "Шаги:\n"
        "1) Ввести телефон в поле 'Телефон' данные '+7 908 777'\n"
        "2) Ввести пароль в поле 'Пароль' данные 'Gub89087814701'\n"
        "3) Нажать на кнопку 'Войти'\n\n"
        "Ожидаемый результат:\n"
        "1) Названия полей телефон/пароль окрашиваются в красный, под полем отображается ошибка\n"
        "2) Пользователь не авторизован\n"
        "3) Пользователь остается на url: https://app.rizz.market/auth/sign-in"
    )
    def test_auth_06_invalid_phone_format(self, sign_in_page: SignInPage):
        # Предусловие: открыть страницу авторизации и форму
        sign_in_page.visit()
        sign_in_page.click_other_methods_button()

        # 1) Ввести телефон в поле "Телефон" данные "+7 908 777"
        sign_in_page.login_form.fill_phone(phone="908777")

        # 2) Ввести пароль в поле "Пароль" данные "Gub89087814701"
        sign_in_page.login_form.fill_password(password="Gub89087814701")

        # 3) Нажать на кнопку "Войти"
        sign_in_page.click_login_button()

        # ОР 1) Названия полей окрашиваются в красный
        sign_in_page.login_form.check_phone_has_error()

        # ОР 3) Пользователь остается на url: .../auth/sign-in
        sign_in_page.check_visible_sign_in_page()
