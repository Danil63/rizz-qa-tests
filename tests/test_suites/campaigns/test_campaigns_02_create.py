"""campaigns-02: Успешное создание рекламной кампании с рандомными данными.

Сценарий:
    1) Страница /app/advertiser/campaigns
    2) Нажать "+ Создать"
    3) Переход на /app/advertiser/campaigns/create
    4) Заполнить все поля рандомными данными
    5) Выключить Автоодобрение
    6) Нажать "Создать кампанию"
    7) Редирект на /app/advertiser/campaigns
    8) Ожидание 3 секунды
"""
import time

import allure
import pytest
from playwright.sync_api import Page

from tests.pages.campaigns_page import CampaignsPage
from tests.pages.create_campaign_page import CreateCampaignPage
from tests.test_data.campaign_generator import generate_campaign_data


@pytest.mark.regression
@pytest.mark.campaigns
@allure.epic("Кампании рекламодателя")
@allure.feature("Создание кампании")
@allure.story("Успешное создание кампании с заполнением всех полей")
@allure.tag("Regression", "Campaigns", "Positive")
class TestCampaigns02:
    """campaigns-02: Создание кампании — Бартер, Ig все форматы, рандомные данные."""

    @allure.title(
        "campaigns-02: Кампании → + Создать → заполнить все поля → Создать кампанию → редирект"
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description(
        "Шаги:\n"
        "1) Открыть страницу списка кампаний\n"
        '2) Нажать кнопку "+ Создать"\n'
        "3) Перейти на страницу создания кампании\n"
        "4) Заполнить Название (рандом)\n"
        "5) Выбрать предмет рекламы — поиск по названию продукта\n"
        "6) Заполнить Ссылку с UTM (рандом)\n"
        "7) Формат контента — Ig: все 3 формата (История, Пост, Reels)\n"
        "8) Тематика — рандомная из списка\n"
        "9) Задание — по шаблону с ключевым запросом и отзывом\n"
        "10) Тип оплаты — Бартер (по умолчанию)\n"
        "11) Максимальная компенсация — цена продукта +20% + рандом до 200₽\n"
        "12) Автоодобрение откликов — ВЫКЛЮЧИТЬ\n"
        '13) Нажать "Создать кампанию"\n\n'
        "Ожидаемый результат:\n"
        "Редирект на https://app.rizz.market/app/advertiser/campaigns"
    )
    def test_campaigns_02_create(
        self,
        campaigns_page: CampaignsPage,
        page: Page,
    ):
        # Генерируем рандомные данные
        data = generate_campaign_data(
            product_name="Гвозди",
            product_price=75,
        )

        # Логируем в Allure
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

        # 1) Страница кампаний уже открыта через фикстуру

        # 2) Нажать "+ Создать"
        campaigns_page.click_create()

        # 3) Проверяем переход на страницу создания
        create_page = CreateCampaignPage(page)
        create_page.expect_loaded()
        create_page.accept_cookies()

        # 4) Название
        create_page.fill_name(data.name)

        # 5) Предмет рекламы
        create_page.select_product_by_search(data.product_search)

        # 6) Ссылка с UTM
        create_page.fill_utm_link(data.utm_link)

        # 7) Формат контента — Ig все 3
        create_page.select_ig_all_formats()

        # 8) Тематика
        create_page.select_thematic(data.thematic)

        # 9) Задание
        create_page.fill_task(data.task)

        # 10) Тип оплаты — Бартер (по умолчанию, не трогаем)

        # 11) Максимальная компенсация
        create_page.fill_max_compensation(data.max_compensation)

        # 12) Автоодобрение — выключить
        create_page.toggle_auto_approve_off()

        # 13) Создать кампанию
        create_page.click_create_campaign()

        # ОР) Редирект на страницу списка кампаний
        result_page = CampaignsPage(page)
        result_page.expect_loaded()

        # Ожидание 3 секунды
        time.sleep(3)
