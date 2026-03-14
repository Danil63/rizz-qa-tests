"""auth-01: Авторизация пользователя по валидным данным."""

import pytest

from tests.pages.campaigns_page import CampaignsPage
from tests.pages.sign_in_page import SignInPage


@pytest.mark.regression
@pytest.mark.authorization
class TestAuth01:
    """auth-01: Авторизация пользователя по валидным данным.

    Предусловие:
        телефон: +7 908 781 4701
        Пароль: 89087814701
    """

    def test_auth_01_valid_login(
        self,
        sign_in_page: SignInPage,
        campaigns_page: CampaignsPage,
    ):
        # 1) Перейти на страницу авторизации
        sign_in_page.visit()

        # 2) Нажать на кнопку "Другие способы входа"
        sign_in_page.click_other_methods_button()

        # 4) В поле Телефон посимвольно ввести данные: +7 908 781 4701
        sign_in_page.login_form.fill_phone(phone="9087814701")

        # 5) В поле пароль посимвольно ввести данные: 89087814701
        sign_in_page.login_form.fill_password(password="89087814701")

        # 6) Нажать на кнопку войти
        sign_in_page.click_login_button()

        # ОР 1) Пользователь переходит на url: .../app/advertiser/campaigns
        campaigns_page.expect_loaded()
