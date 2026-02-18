"""campaigns-01: Успешное создание рекламной кампании с рандомными данными."""
import allure
import pytest
from playwright.sync_api import Page

from tests.pages.create_campaign_page import CreateCampaignPage
from tests.pages.campaigns_page import CampaignsPage
from tests.test_data.campaign_generator import generate_campaign_data


@pytest.mark.regression
@pytest.mark.campaigns
@allure.epic("Кампании рекламодателя")
@allure.feature("Создание кампании")
@allure.story("Успешное создание кампании с заполнением всех полей")
@allure.tag("Regression", "Campaigns", "Positive")
class TestCampaigns01:
    """campaigns-01: Создание кампании — Бартер, Ig все форматы, рандомные данные."""

    @allure.title(
        "campaigns-01: Заполнение всех полей → Создать кампанию → редирект на /campaigns"
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description(
        "Шаги:\n"
        "1) Открыть страницу создания кампании\n"
        "2) Заполнить Название (рандом)\n"
        "3) Выбрать предмет рекламы — поиск по названию продукта\n"
        "4) Заполнить Ссылку с UTM (рандом)\n"
        "5) Формат контента — Ig: все 3 формата (История, Пост, Reels)\n"
        "6) Тематика — рандомная из списка\n"
        "7) Задание — по шаблону с ключевым запросом и отзывом\n"
        "8) Тип оплаты — Бартер (по умолчанию)\n"
        "9) Максимальная компенсация — цена продукта +20% + рандом до 200₽\n"
        "10) Автоодобрение откликов — ВЫКЛЮЧИТЬ\n"
        '11) Нажать "Создать кампанию"\n\n'
        "Ожидаемый результат:\n"
        "Редирект на https://app.rizz.market/app/advertiser/campaigns"
    )
    def test_campaigns_01_create(
        self,
        create_campaign_page: CreateCampaignPage,
        page: Page,
    ):
        # Генерируем рандомные данные
        data = generate_campaign_data(
            product_name="Гвозди",
            product_price=75,
        )

        # Логируем в Allure что именно сгенерировали
        allure.attach(
            f"Название: {data.name}\n"
            f"Предмет рекламы (поиск): {data.product_search}\n"
            f"UTM-ссылка: {data.utm_link}\n"
            f"Тематика: {data.thematic}\n"
            f"Макс. компенсация: {data.max_compensation} ₽\n"
            f"Задание:\n{data.task}",
            name="Сгенерированные данные кампании",
            attachment_type=allure.attachment_type.TEXT,
        )

        # 1) Страница уже открыта через фикстуру

        # 2) Название
        create_campaign_page.fill_name(data.name)

        # 3) Предмет рекламы
        create_campaign_page.select_product_by_search(data.product_search)

        # 4) Ссылка с UTM
        create_campaign_page.fill_utm_link(data.utm_link)

        # 5) Формат контента — Ig все 3
        create_campaign_page.select_ig_all_formats()

        # 6) Тематика
        create_campaign_page.select_thematic(data.thematic)

        # 7) Задание
        create_campaign_page.fill_task(data.task)

        # 8) Тип оплаты — Бартер (по умолчанию, не трогаем)

        # 9) Максимальная компенсация
        create_campaign_page.fill_max_compensation(data.max_compensation)

        # 10) Автоодобрение — выключить
        create_campaign_page.toggle_auto_approve_off()

        # 11) Создать кампанию
        create_campaign_page.click_create_campaign()

        # ОР) Редирект на страницу списка кампаний
        campaigns = CampaignsPage(page)
        campaigns.expect_loaded()
