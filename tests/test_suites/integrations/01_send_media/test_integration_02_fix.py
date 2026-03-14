"""integration-02: Выполнение интеграции блогером (fix-кампания)."""

import json
from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

from tests.pages.integration_page import IntegrationPage

WORKS_URL = "https://app.rizz.market/app/creator/works?filter=New"
ADVERTISER_BASE = "https://app.rizz.market/app/advertiser/campaigns"
LAST_PRODUCT_TWO_META_PATH = (
    Path(__file__).resolve().parents[3] / "test_data" / "last_product_two_meta.json"
)
FIX_CAMPAIGN_CONTEXT_PATH = (
    Path(__file__).resolve().parents[3] / "test_data" / "fix_campaing_context.json"
)
FIX_INTEGRATIONS_PATH = (
    Path(__file__).resolve().parents[3] / "test_data" / "fix_integrations.json"
)
TEST_VIDEO_PATH = str(
    Path(__file__).resolve().parents[3] / "test_data" / "sample-5s.mp4"
)


@pytest.mark.regression
@pytest.mark.integrations
class TestIntegration02Fix:
    def test_execute_fix_integration(self, blogger_page: Page):
        page = IntegrationPage(blogger_page)

        # Переходим на страницу интеграций (filter=New)
        blogger_page.goto(WORKS_URL, wait_until="networkidle")
        blogger_page.wait_for_timeout(3000)

        # Получаем название продукта из last_product_two_meta.json
        product_name = self._resolve_product_name(blogger_page)

        # Клик по карточке продукта
        card = blogger_page.locator("span.line-clamp-2", has_text=product_name).first
        expect(card).to_be_visible(timeout=15000)
        card.click()

        # Сохраняем URLs интеграции для последующих тестов
        blogger_page.wait_for_url("**/works/**", timeout=10000)
        creator_url = blogger_page.url
        integration_id = creator_url.rstrip("/").split("/")[-1]
        campaign_context = json.loads(
            FIX_CAMPAIGN_CONTEXT_PATH.read_text(encoding="utf-8")
        )
        campaign_id = campaign_context["campaign_id"]
        advertiser_url = f"{ADVERTISER_BASE}/{campaign_id}/works/{integration_id}"
        FIX_INTEGRATIONS_PATH.write_text(
            json.dumps(
                {
                    "creator": creator_url,
                    "advertiser": advertiser_url,
                    "campaign_id": campaign_id,
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

    # Проверяем переход на страницу интеграции
        expect(
            blogger_page.get_by_role("heading", name="Подтвердите начало работы")
        ).to_be_visible(timeout=5000)

    # Нажать кнопку "Товар выкуплен"
        blogger_page.get_by_role("button", name="Товар выкуплен").click()

    # Проверяем появление заголовка "Шаги выкупа товара"
        expect(
            blogger_page.get_by_role("heading", name="Шаги выкупа товара")
        ).to_be_visible(timeout=5000)

        # Загрузка изображений для первых 2 шагов
        page.upload_all_media_steps(count=2)

    # Шаг 3 — Медиа-контент (видео): просто загрузить и отправить
        video_input = blogger_page.locator(
            '//h3[text()="Медиа-контент"]/following::input[@accept="video/*"][1]'
        )
        expect(video_input).to_be_attached(timeout=15000)
        video_input.set_input_files(TEST_VIDEO_PATH)
        blogger_page.wait_for_timeout(5000)
        blogger_page.get_by_role("button", name="Отправить", exact=True).first.click()
        blogger_page.wait_for_timeout(3000)

    @staticmethod
    def _resolve_product_name(browser_page: Page) -> str:
        """Получить название продукта.

        1) Из last_product_two_meta.json если файл существует.
        2) Иначе — берём заголовок первой карточки на странице.
        """
        if LAST_PRODUCT_TWO_META_PATH.exists():
            meta = json.loads(LAST_PRODUCT_TWO_META_PATH.read_text(encoding="utf-8"))
            name = (meta.get("name") or "").strip()
            if name:
                return name

        # Fallback: первая карточка на странице
        first_card = browser_page.locator("span.line-clamp-2").first
        expect(first_card).to_be_visible(timeout=15000)
        return first_card.inner_text().strip()
