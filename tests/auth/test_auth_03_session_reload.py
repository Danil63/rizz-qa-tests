"""auth-03: Сохранение сессии после перезагрузки."""
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
class TestAuth03:

    @allure.title("auth-03: Сохранение сессии после перезагрузки")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description(
        "Проверка сохранения авторизованной сессии после перезагрузки страницы. "
        "Пользователь должен остаться на странице кампаний."
    )
    def test_auth_03_session_persists_after_reload(self, sign_in_page: SignInPage, campaigns_page: CampaignsPage):
        sign_in_page.visit("https://app.rizz.market/auth/sign-in")
        sign_in_page.click_other_methods_button()
        sign_in_page.login_form.fill(phone="+79087814701", password="89087814701")
        sign_in_page.click_login_button()
        campaigns_page.expect_loaded()
        campaigns_page.reload()
        campaigns_page.expect_loaded()
