"""campaigns-04: Успешное создание рекламной кампании — За просмотры, Услуга, Ig все форматы.

Сценарий:
    1) Страница /app/advertiser/campaigns
    2) Нажать "+ Создать"
    3) Переход на /app/advertiser/campaigns/create
    4) ПЕРВОЕ ДЕЙСТВИЕ: Тип оплаты — За просмотры
    5) Заполнить Название (рандом)
    6) Выбрать услугу по названию из last_service_meta.json (вкладка "Услуги")
    7) Заполнить Ссылку с UTM (рандом)
    8) Формат контента — Ig: все 3 формата
    9) Тематика — рандомная
    10) Задание — рандомный шаблон
    11) Минимальный охват блогера — 90
    12) Максимальная выплата блогеру — 100
    13) Автоодобрение — ВЫКЛЮЧИТЬ
    14) Нажать "Создать кампанию"
    15) Редирект на /app/advertiser/campaigns
"""

import json
import re
import time
from pathlib import Path

import allure
import pytest
from playwright.sync_api import Page

from tests.pages.campaigns_page import CampaignsPage
from tests.pages.create_campaign_page import CreateCampaignPage
from tests.test_data.campaign_generator import generate_campaign_data

LAST_CAMPAIGN_CONTEXT_PATH = (
    Path(__file__).resolve().parents[2] / "test_data" / "last_campaign_context.json"
)
LAST_SERVICE_META_PATH = (
    Path(__file__).resolve().parents[2] / "test_data" / "last_service_meta.json"
)
INTEGRATIONS_PATH = (
    Path(__file__).resolve().parents[2] / "test_data" / "integrations.json"
)


@pytest.mark.regression
@pytest.mark.campaigns
@allure.epic("Кампании рекламодателя")
@allure.feature("Создание кампании")
@allure.story("Успешное создание кампании — За просмотры, Услуга, Ig все форматы")
@allure.tag("Regression", "Campaigns", "Positive")
class TestCampaigns04:
    """campaigns-04: Создание кампании — За просмотры, Услуга, Ig все форматы, рандомные данные."""

    @staticmethod
    def _save_campaign_id(campaign_id: str) -> None:
        """Сохранить campaign_id в integrations.json."""
        data: dict = {}
        if INTEGRATIONS_PATH.exists():
            try:
                data = json.loads(INTEGRATIONS_PATH.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, ValueError):
                data = {}
        data["campaign_id"] = campaign_id
        INTEGRATIONS_PATH.write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    @allure.title(
        "campaigns-04: Кампании → + Создать → За просмотры → Услуга → заполнить все поля → Создать кампанию → редирект"
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description(
        "Шаги:\n"
        "1) Открыть страницу списка кампаний\n"
        '2) Нажать кнопку "+ Создать"\n'
        "3) Перейти на страницу создания кампании\n"
        "4) ПЕРВОЕ ДЕЙСТВИЕ: выбрать тип оплаты 'За просмотры'\n"
        "5) Заполнить Название (рандом)\n"
        "6) Выбрать услугу по названию из last_service_meta.json (вкладка 'Услуги')\n"
        "7) Заполнить Ссылку с UTM (рандом)\n"
        "8) Формат контента — Ig: все 3 формата (История, Пост, Reels)\n"
        "9) Тематика — рандомная из списка\n"
        "10) Задание — по шаблону с ключевым запросом и отзывом\n"
        "11) Минимальный охват блогера — 90\n"
        "12) Максимальная выплата блогеру — 100\n"
        "13) Автоодобрение откликов — ВЫКЛЮЧИТЬ\n"
        '14) Нажать "Создать кампанию"\n\n'
        "Ожидаемый результат:\n"
        "Редирект на https://app.rizz.market/app/advertiser/campaigns"
    )
    def test_campaigns_04_create(
        self,
        campaigns_page: CampaignsPage,
        page: Page,
    ):
        assert LAST_SERVICE_META_PATH.exists(), (
            f"Файл с метаданными услуги не найден: {LAST_SERVICE_META_PATH}. "
            "Сначала запусти тест создания услуги."
        )
        service_meta = json.loads(LAST_SERVICE_META_PATH.read_text(encoding="utf-8"))
        service_name = (service_meta.get("name") or "").strip()
        assert service_name, "Поле name в last_service_meta.json пустое"

        # Генерируем рандомные данные кампании (name, utm_link, thematic, task)
        data = generate_campaign_data(product_name=service_name, product_price=0)

        # Сохраняем контекст кампании для последующих проверок
        LAST_CAMPAIGN_CONTEXT_PATH.parent.mkdir(parents=True, exist_ok=True)
        category = service_meta.get("category") or ""

        LAST_CAMPAIGN_CONTEXT_PATH.write_text(
            json.dumps(
                {
                    "campaign_title": data.name,
                    "category": category,
                    "reward": "За просмотры",
                    "social_network": "Ig",
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        # Логируем в Allure
        allure.attach(
            f"Название: {data.name}\n"
            f"Услуга (поиск): {service_name}\n"
            f"UTM-ссылка: {data.utm_link}\n"
            f"Тематика: {data.thematic}\n"
            f"Минимальный охват: 90\n"
            f"Макс. выплата: 100 ₽\n"
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

        # 4) ПЕРВОЕ ДЕЙСТВИЕ: тип оплаты — За просмотры
        create_page.select_per_views_tab()

        # 5) Название
        create_page.fill_name(data.name)

        # 6) Предмет рекламы — Услуга
        create_page.select_service_by_search(service_name)

        # 7) Ссылка с UTM
        create_page.fill_utm_link(data.utm_link)

        # 8) Формат контента — Ig все 3
        create_page.select_ig_all_formats()

        # 9) Тематика
        create_page.select_thematic(data.thematic)

        # 10) Задание
        create_page.fill_task(data.task)

        # 11) Минимальный охват блогера
        create_page.fill_min_coverage("90")

        # 12) Максимальная выплата блогеру
        create_page.fill_max_payout("100")

        # 13) Автоодобрение — выключить
        create_page.toggle_auto_approve_off()

        # 14) Создать кампанию
        create_page.click_create_campaign()

        page.wait_for_timeout(5000)

        # ОР) Ожидание редиректа на страницу кампаний
        from playwright.sync_api import expect as pw_expect

        pw_expect(page).to_have_url(
            re.compile(r".*/app/advertiser/campaigns.*"), timeout=14000
        )

        time.sleep(5)

        # Сохранить campaign_id в integrations.json
        href = campaigns_page.first_campaign_link.get_attribute("href") or ""
        match = re.search(
            r"/campaigns/([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})",
            href,
        )
        if match:
            self._save_campaign_id(match.group(1))
