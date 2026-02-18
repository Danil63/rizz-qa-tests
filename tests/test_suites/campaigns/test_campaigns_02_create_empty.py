"""campaigns-02: Негативный тест — создание кампании без заполнения полей."""
import allure
import pytest
from playwright.sync_api import Page

from tests.pages.create_campaign_page import CreateCampaignPage


@pytest.mark.regression
@pytest.mark.campaigns
@allure.epic("Кампании рекламодателя")
@allure.feature("Создание кампании")
@allure.story("Валидация обязательных полей при пустой отправке")
@allure.tag("Regression", "Campaigns", "Negative", "Validation")
class TestCampaigns02:
    """campaigns-02: Нажатие «Создать кампанию» без заполнения полей."""

    @allure.title(
        "campaigns-02: Пустая форма → Создать кампанию → 5 ошибок валидации"
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description(
        "Шаги:\n"
        "1) Открыть страницу создания кампании\n"
        "2) Не заполнять ни одно поле\n"
        '3) Нажать "Создать кампанию"\n\n'
        "Ожидаемый результат:\n"
        "1) Остаёмся на странице /app/advertiser/campaigns/create\n"
        "2) Отображаются 5 ошибок валидации:\n"
        '   — Название: "Обязательное поле"\n'
        '   — Предмет рекламы: "Обязательное поле"\n'
        '   — Формат контента: "Необходимо выбрать социальную сеть"\n'
        '   — Тематика: "Нужно выбрать хотя бы одну тематику."\n'
        '   — Задание: "Значение слишком маленькое. Минимум: 5"'
    )
    def test_campaigns_02_create_empty(
        self,
        create_campaign_page: CreateCampaignPage,
        page: Page,
    ):
        # 1) Страница уже открыта через фикстуру

        # 2) Не заполняем ни одно поле

        # 3) Нажать "Создать кампанию"
        create_campaign_page.click_create_campaign()

        # Небольшая пауза для появления ошибок
        page.wait_for_timeout(1000)

        # ОР-1) URL остаётся на странице создания
        create_campaign_page.check_still_on_create_page()

        # ОР-2) Проверяем общее количество ошибок
        create_campaign_page.check_all_validation_errors_visible()

        # ОР-3) Проверяем каждую ошибку по отдельности
        create_campaign_page.check_error_name()
        create_campaign_page.check_error_product()
        create_campaign_page.check_error_content_format()
        create_campaign_page.check_error_thematic()
        create_campaign_page.check_error_task()
