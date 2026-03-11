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

FIX_CAMPAIGN_CONTEXT_PATH = (
    Path(__file__).resolve().parents[2] / "test_data" / "fix_campaing_context.json"
)
LAST_PRODUCT_TWO_META_PATH = (
    Path(__file__).resolve().parents[2] / "test_data" / "last_product_two_meta.json"
)


@pytest.mark.regression
@pytest.mark.campaigns
@allure.epic("Кампании рекламодателя")
@allure.feature("Создание кампании")
@allure.story("Успешное создание кампании с заполнением всех полей")
@allure.tag("Regression", "Campaigns", "Positive")
class TestCampaigns02:
    """campaigns-02: Создание кампании — Бартер, Ig все форматы, рандомные данные."""

    @staticmethod
    def _save_campaign_id(campaign_id: str) -> None:
        """Добавить campaign_id в fix_campaing_context.json."""
        data: dict = {}
        if FIX_CAMPAIGN_CONTEXT_PATH.exists():
            try:
                data = json.loads(FIX_CAMPAIGN_CONTEXT_PATH.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, ValueError):
                data = {}
        data["campaign_id"] = campaign_id
        FIX_CAMPAIGN_CONTEXT_PATH.write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )

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
        assert LAST_PRODUCT_TWO_META_PATH.exists(), (
            f"Файл с метаданными продукта не найден: {LAST_PRODUCT_TWO_META_PATH}. "
            "Сначала запусти тест создания продукта."
        )
        product_meta = json.loads(LAST_PRODUCT_TWO_META_PATH.read_text(encoding="utf-8"))
        product_name = (product_meta.get("name") or "").strip()
        assert product_name, "Поле name в last_product_meta.json пустое"

        # Генерируем данные кампании с использованием сохраненного названия продукта
        data = generate_campaign_data(product_name=product_name, product_price=75)

        # Сохраняем контекст кампании в JSON для последующих проверок
        FIX_CAMPAIGN_CONTEXT_PATH.parent.mkdir(parents=True, exist_ok=True)

        marketplace = product_meta.get("marketplace") or "Ozon"
        category = product_meta.get("category") or "Спорт и отдых"

        existing: dict = {}
        if FIX_CAMPAIGN_CONTEXT_PATH.exists():
            try:
                existing = json.loads(FIX_CAMPAIGN_CONTEXT_PATH.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, ValueError):
                existing = {}
        price_list = existing.get("price", [])
        price_list.append(data.max_compensation)
        FIX_CAMPAIGN_CONTEXT_PATH.write_text(
            json.dumps(
                {
                    **existing,
                    "campaign_title": data.name,
                    "marketplace": marketplace,
                    "category": category,
                    "reward": "Фиксированная",
                    "social_network": "Ig",
                    "price": price_list,
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
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

        # 10) Тип оплаты — Фиксированная 
        create_page.check_fixded_tab_selected()

        # 11) Вознаграждение
        create_page.input_reward(data.max_compensation)

        # 12) Автоодобрение — выключить
        create_page.toggle_auto_approve_off()

        # 13) Создать кампанию
        create_page.click_create_campaign()

        page.wait_for_timeout(5000)

        # ОР) Ожидание редиректа на страницу кампаний (до 10 секунд)
        from playwright.sync_api import expect as pw_expect

        pw_expect(page).to_have_url(
            re.compile(r".*/app/advertiser/campaigns.*"), timeout=14000
        )

        # Ожидание 3 секунды
        time.sleep(5)

        # Сохранить campaign_id в fix_campaing_context.json
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
