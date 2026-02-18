"""auth-02: Повторная авторизация по валидным данным."""
import allure
import pytest

from tests.pages.sign_in_page import SignInPage
from tests.pages.campaigns_page import CampaignsPage


@pytest.mark.regression
@pytest.mark.authorization
@allure.epic("Авторизация")
@allure.feature("Вход по телефону")
@allure.story("Успешная авторизация")
@allure.tag("Regression", "Authorization")
class TestAuth02:
    """auth-02: Повторная авторизация по валидным данным.

    Предусловие:
        телефон: +7 908 781 4701
        Пароль: Gub89087814701
    """

    @allure.title("auth-02: Повторная авторизация по валидным данным")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description(
        "Шаги:\n"
        "1) Перейти на url: https://rizz.market/\n"
        "2) Нажать на кнопку 'Подключиться к платформе'\n"
        "3) Нажать на кнопку 'Другие способы входа'\n"
        "4) В поле Телефон посимвольно ввести данные: +7 908 781 4701\n"
        "5) В поле пароль посимвольно ввести данные: 89087814701\n"
        "6) Нажать на кнопку войти\n\n"
        "Ожидаемый результат:\n"
        "1) Пользователь переходит на url: https://app.rizz.market/app/advertiser/campaigns\n"
        "2) Пользователь видит заголовок 'Кампании'"
    )
    def test_auth_02_repeat_login(
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
