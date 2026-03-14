"""auth-05: Отображение ошибки по невалидному телефону."""

import pytest

from tests.pages.sign_in_page import SignInPage


@pytest.mark.regression
@pytest.mark.authorization
class TestAuth05:
    """auth-05: Отображение ошибки по невалидному телефону.

    Предусловие:
        телефон: +7 908 777
        Пароль: Gub89087814701
    """

    def test_auth_05_invalid_phone_format(self, sign_in_page: SignInPage):
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
