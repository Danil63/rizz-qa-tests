"""campaigns-01: Негативный тест — создание кампании без заполнения полей.

Сценарий:
    1) Страница /app/advertiser/campaigns
    2) Нажать "+ Создать"
    3) Переход на /app/advertiser/campaigns/create
    4) Не заполнять ни одно поле
    5) Нажать "Создать кампанию"
    6) Проверить 5 ошибок валидации
"""
import allure
import pytest
from playwright.sync_api import Page

from tests.pages.campaigns_page import CampaignsPage
from tests.pages.create_campaign_page import CreateCampaignPage


@pytest.mark.regression
@pytest.mark.campaigns
@allure.epic("Кампании рекламодателя")
@allure.feature("Создание кампании")
@allure.story("Валидация обязательных полей при пустой отправке")
@allure.tag("Regression", "Campaigns", "Negative", "Validation")
class TestCampaigns01:
    """campaigns-01: Нажатие «Создать кампанию» без заполнения полей."""

    @allure.title(
        "campaigns-01: Кампании → + Создать → пустая форма → Создать кампанию → 5 ошибок"
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description(
        "Шаги:\n"
        "1) Открыть страницу списка кампаний\n"
        '2) Нажать кнопку "+ Создать"\n'
        "3) Перейти на страницу создания кампании\n"
        "4) Не заполнять ни одно поле\n"
        '5) Нажать "Создать кампанию"\n\n'
        "Ожидаемый результат:\n"
        "1) Остаёмся на странице /app/advertiser/campaigns/create\n"
        "2) Отображаются 5 ошибок валидации:\n"
        '   — Название: "Обязательное поле"\n'
        '   — Предмет рекламы: "Обязательное поле"\n'
        '   — Формат контента: "Необходимо выбрать социальную сеть"\n'
        '   — Тематика: "Нужно выбрать хотя бы одну тематику."\n'
        '   — Задание: "Значение слишком маленькое. Минимум: 5"'
    )
    def test_campaigns_01_create_empty(
        self,
        campaigns_page: CampaignsPage,
        page: Page,
    ):
        # 1) Страница кампаний уже открыта через фикстуру

        # 2) Нажать "+ Создать"
        campaigns_page.click_create()

        # 3) Проверяем переход на страницу создания
        create_page = CreateCampaignPage(page)
        create_page.expect_loaded()
        create_page.accept_cookies()

        # 4) Не заполняем ни одно поле

        # 5) Нажать "Создать кампанию"
        create_page.click_create_campaign()

        # Пауза для появления ошибок
        page.wait_for_timeout(1000)

        # ОР-1) URL остаётся на странице создания
        create_page.check_still_on_create_page()

        # ОР-2) Общее количество ошибок ≥ 5
        create_page.check_all_validation_errors_visible()

        # ОР-3) Каждая ошибка по отдельности
        create_page.check_error_name()
        create_page.check_error_product()
        create_page.check_error_content_format()
        create_page.check_error_thematic()
        create_page.check_error_task()
