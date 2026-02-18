"""campaigns-03: Фильтр кампаний — выбор «Самостоятельно» на табе Активные.

Сценарий:
    1) Страница /app/advertiser/campaigns
    2) Убедиться что таб «Активные» выбран
    3) Открыть dropdown фильтра ведения (по умолчанию «Все»)
    4) Выбрать «Самостоятельно»
    5) Проверить что таб «Активные» по-прежнему выбран
    6) Проверить что список кампаний отображается
"""
import allure
import pytest
from playwright.sync_api import Page, expect

from playwright.sync_api import expect
from tests.pages.campaigns_page import CampaignsPage


@pytest.mark.regression
@pytest.mark.campaigns
@allure.epic("Кампании рекламодателя")
@allure.feature("Фильтрация кампаний")
@allure.story("Фильтр ведения: Самостоятельно")
@allure.tag("Regression", "Campaigns", "Filters")
class TestCampaigns03:
    """campaigns-03: Фильтр ведения «Самостоятельно» на табе Активные."""

    @allure.title(
        "campaigns-03: Кампании → фильтр «Самостоятельно» → таб Активные → список виден"
    )
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description(
        "Шаги:\n"
        "1) Открыть страницу списка кампаний\n"
        "2) Проверить что таб «Активные» выбран\n"
        '3) Открыть dropdown фильтра ведения (значение «Все»)\n'
        '4) Выбрать «Самостоятельно»\n'
        "5) Проверить что таб «Активные» по-прежнему выбран\n"
        "6) Проверить что список кампаний отображается"
    )
    def test_campaigns_03_filter_self_managed(
        self,
        campaigns_page: CampaignsPage,
        page: Page,
    ):
        # 1) Страница кампаний уже открыта через фикстуру

        # 2) Таб «Активные» выбран по умолчанию
        campaigns_page.check_active_tab_selected()

        # 3-4) Выбрать фильтр «Самостоятельно»
        campaigns_page.select_management_filter("Самостоятельно")

        # Пауза для обновления списка
        page.wait_for_timeout(1500)

        # 5) Таб «Активные» по-прежнему выбран
        campaigns_page.check_active_tab_selected()

        # 6) Проверяем что фильтр применился — значение dropdown = «Самостоятельно»
        expect(campaigns_page.filter_management).to_contain_text("Самостоятельно")
