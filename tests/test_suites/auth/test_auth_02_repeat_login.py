"""auth-02: Повторная авторизация по валидным данным."""
import allure
import pytest

from tests.pages.sign_in_page import SignInPage
from tests.pages.market_page import MarketPage


@pytest.mark.regression
@pytest.mark.authorization
@allure.epic("Авторизация")
@allure.feature("Вход по телефону")
@allure.story("Успешная авторизация")
@allure.tag("Regression", "Authorization")
class TestAuth02:
    """auth-02: Повторная авторизация по валидным данным.

    Предусловие:
        телефон: +7 993 885 4791
        Пароль: 89087814701
    """

    @allure.title("auth-02: Повторная авторизация по валидным данным")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description(
        "Шаги:\n"
        "1) Перейти на страницу авторизации\n"
        "2) Нажать на кнопку 'Другие способы входа'\n"
        "3) В поле Телефон посимвольно ввести данные: +7 993 885 4791\n"
        "4) В поле пароль посимвольно ввести данные: 89087814701\n"
        "5) Нажать на кнопку войти\n\n"
        "Ожидаемый результат:\n"
        "1) Пользователь переходит на url: https://app.rizz.market/app/creator/market\n"
        "2) Пользователь авторизован"
    )
    def test_auth_02_repeat_login(
        self,
        sign_in_page: SignInPage,
        market_page: MarketPage,
    ):
        # 1) Перейти на страницу авторизации
        sign_in_page.visit()

        # 2) Нажать на кнопку "Другие способы входа"
        sign_in_page.click_other_methods_button()

        # 3) В поле Телефон посимвольно ввести данные: +7 993 885 4791
        sign_in_page.login_form.fill_phone(phone="9938854791")

        # 4) В поле пароль посимвольно ввести данные: 89087814701
        sign_in_page.login_form.fill_password(password="89087814701")

        # 5) Нажать на кнопку войти
        sign_in_page.click_login_button()

        # ОР 1) Пользователь переходит на маркет блогера
        market_page.expect_loaded()
