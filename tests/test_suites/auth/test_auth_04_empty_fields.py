"""auth-04: Отображение ошибки при игнорировании заполнения обязательных полей."""

import pytest

from tests.pages.sign_in_page import SignInPage


@pytest.mark.regression
@pytest.mark.authorization
class TestAuth04:
    """auth-04: Отображение ошибки при игнорировании заполнения обязательных полей."""

    def test_auth_04_empty_fields(self, sign_in_page: SignInPage):
        # Предусловие: открыть страницу авторизации и форму
        sign_in_page.visit()
        sign_in_page.click_other_methods_button()

        # 1) Нажать на кнопку "Войти" проигнорировав заполнение обязательных полей
        sign_in_page.click_login_button()

        # ОР 1) Поле пароля подсвечено ошибкой + текст "Обязательное поле"
        sign_in_page.login_form.check_password_has_error()
        sign_in_page.login_form.check_password_error_message("Обязательное поле")

        # ОР 3) Пользователь остается на url: .../auth/sign-in
        sign_in_page.check_visible_sign_in_page()
