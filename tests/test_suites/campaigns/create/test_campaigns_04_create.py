"""campaigns-04: Успешное создание рекламной кампании — За просмотры, Услуга, Ig все форматы.

Сценарий:
    1) Страница /app/advertiser/campaigns
    2) Нажать "+ Создать"
    3) Переход на /app/advertiser/campaigns/create
    4) ПЕРВОЕ ДЕЙСТВИЕ: Тип оплаты — За просмотры
    5) Заполнить Название (рандом)
    6) Выбрать услугу по названию из last_service_meta.json (вкладка "Услуги")
    7) Заполнить Ссылку с UTM (рандом)
    8) Формат контента — TikTok: Видео
    9) Тематика — рандомная
    10) Задание — рандомный шаблон
    11) Минимальный охват блогера — 90
    12) Максимальная выплата блогеру — 100
    13) Нажать "Создать кампанию"
    14) Редирект на /app/advertiser/campaigns
"""

import json
import random
import re
import time
from pathlib import Path

import pytest
from playwright.sync_api import Page

from tests.pages.campaigns_page import CampaignsPage
from tests.pages.create_campaign_page import CreateCampaignPage
from tests.test_data.campaign_generator import generate_campaign_data

CPM_CAMPAIGN_CONTEXT_PATH = (
    Path(__file__).resolve().parents[3] / "test_data" / "cpm_campaign_context.json"
)
LAST_SERVICE_META_PATH = (
    Path(__file__).resolve().parents[3] / "test_data" / "last_service_meta.json"
)


@pytest.mark.skip(reason="Temporarily skipped")
@pytest.mark.regression
@pytest.mark.campaigns
class TestCampaigns04:
    """campaigns-04: Создание кампании — За просмотры, Услуга, TikTok Видео, рандомные данные."""

    @staticmethod
    def _save_campaign_id(campaign_id: str) -> None:
        """Добавить campaign_id в cpm_campaign_context.json."""
        data: dict = {}
        if CPM_CAMPAIGN_CONTEXT_PATH.exists():
            try:
                data = json.loads(CPM_CAMPAIGN_CONTEXT_PATH.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, ValueError):
                data = {}
        data["campaign_id"] = campaign_id
        CPM_CAMPAIGN_CONTEXT_PATH.write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
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
        CPM_CAMPAIGN_CONTEXT_PATH.parent.mkdir(parents=True, exist_ok=True)
        category = service_meta.get("category") or ""

        existing: dict = {}
        if CPM_CAMPAIGN_CONTEXT_PATH.exists():
            try:
                existing = json.loads(CPM_CAMPAIGN_CONTEXT_PATH.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, ValueError):
                existing = {}
        MAX_PAYOUT = 202
        cpm_price = random.randint(200, 220)
        CPM_CAMPAIGN_CONTEXT_PATH.write_text(
            json.dumps(
                {
                    **existing,
                    "campaign_title": data.name,
                    "category": category,
                    "reward": "За просмотры",
                    "social_network": "TikTok",
                    "price": cpm_price,
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        # Логируем в Allure

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

        # 8) Формат контента — TikTok Видео
        create_page.select_tiktok_video_format()

        # 9) Тематика
        create_page.select_thematic(data.thematic)

        # 10) Задание
        create_page.fill_task(data.task)

        # 11) Цена за 1000 просмотров
        create_page.fill_cpm_price(str(cpm_price))

        # 12) Минимальный охват блогера
        create_page.fill_min_coverage("90")

        # 13) Максимальная выплата блогеру
        create_page.fill_max_payout(str(MAX_PAYOUT))

        # 14) Создать кампанию
        create_page.click_create_campaign()

        page.wait_for_timeout(5000)

        # ОР) Ожидание редиректа на страницу кампаний
        from playwright.sync_api import expect as pw_expect

        pw_expect(page).to_have_url(
            re.compile(r".*/app/advertiser/campaigns.*"), timeout=14000
        )

        time.sleep(5)

        # Сохранить campaign_id в cpm_campaign_context.json
        uuid_pattern = re.compile(
            r"/campaigns/([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})"
        )
        campaign_id_found = None
        deadline = time.time() + 20
        while time.time() < deadline and campaign_id_found is None:
            for link in page.locator('a[href*="/campaigns/"]').all():
                href = link.get_attribute("href") or ""
                m = uuid_pattern.search(href)
                if m:
                    campaign_id_found = m.group(1)
                    break
            if campaign_id_found is None:
                time.sleep(0.5)
        if campaign_id_found:
            self._save_campaign_id(campaign_id_found)
