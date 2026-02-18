"""market-01: Проверка отображения элементов страницы маркета блогера."""
import allure
import pytest

from tests.pages.market_page import MarketPage


@pytest.mark.regression
@pytest.mark.market
@allure.epic("Маркет блогера")
@allure.feature("Страница маркета")
@allure.story("Отображение элементов")
@allure.tag("Regression", "Market", "UI")
class TestMarket01:
    """market-01: Проверка отображения всех ключевых элементов страницы маркета."""

    @allure.title("market-01: Навигация в хедере отображается")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_market_01_navigation_visible(self, market_page: MarketPage):
        market_page.expect_loaded()
        market_page.check_navigation_visible()

    @allure.title("market-01: Аватар пользователя отображается")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_market_01_user_avatar_visible(self, market_page: MarketPage):
        market_page.expect_loaded()
        market_page.check_user_avatar_visible()

    @allure.title("market-01: Поле поиска отображается")
    @allure.severity(allure.severity_level.NORMAL)
    def test_market_01_search_visible(self, market_page: MarketPage):
        market_page.expect_loaded()
        market_page.check_search_visible()

    @allure.title("market-01: Фильтры отображаются")
    @allure.severity(allure.severity_level.NORMAL)
    def test_market_01_filters_visible(self, market_page: MarketPage):
        market_page.expect_loaded()
        market_page.check_filters_visible()

    @allure.title("market-01: Карусель баннеров отображается")
    @allure.severity(allure.severity_level.MINOR)
    def test_market_01_carousel_visible(self, market_page: MarketPage):
        market_page.expect_loaded()
        market_page.check_carousel_visible()

    @allure.title("market-01: Первая карточка кампании отображается")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_market_01_first_card_visible(self, market_page: MarketPage):
        market_page.expect_loaded()
        market_page.first_card.check_visible()
        market_page.first_card.check_has_title()
        market_page.first_card.check_has_price()

    @allure.title("market-01: Реферальный баннер отображается")
    @allure.severity(allure.severity_level.MINOR)
    def test_market_01_referral_banner_visible(self, market_page: MarketPage):
        market_page.expect_loaded()
        market_page.check_referral_banner_visible()

    @allure.title("market-01: Футер отображается")
    @allure.severity(allure.severity_level.MINOR)
    def test_market_01_footer_visible(self, market_page: MarketPage):
        market_page.expect_loaded()
        market_page.check_footer_visible()

    @allure.title("market-01: Бейдж АВТООДОБРЕНИЕ отображается")
    @allure.severity(allure.severity_level.NORMAL)
    def test_market_01_auto_approve_badge(self, market_page: MarketPage):
        market_page.expect_loaded()
        market_page.check_auto_approve_badge_visible()

    @allure.title("market-01: Бейдж НАЛОГ ОПЛАЧЕН отображается")
    @allure.severity(allure.severity_level.NORMAL)
    def test_market_01_tax_paid_badge(self, market_page: MarketPage):
        market_page.expect_loaded()
        market_page.check_tax_paid_badge_visible()

    @allure.title("market-01: Бейдж С МАРКИРОВКОЙ отображается")
    @allure.severity(allure.severity_level.NORMAL)
    def test_market_01_marking_badge(self, market_page: MarketPage):
        market_page.expect_loaded()
        market_page.check_marking_badge_visible()
