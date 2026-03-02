"""integration-01: Выполнение интеграции блогером."""
import json
from pathlib import Path

import allure
import pytest
from playwright.sync_api import Page, expect

from tests.pages.integration_page import IntegrationPage

CHAT_MESSAGE = "Приступаю к выполнению работы"
WORKS_URL = "https://app.rizz.market/app/creator/works?filter=New"
LAST_PRODUCT_META_PATH = (
    Path(__file__).resolve().parents[2] / "test_data" / "last_product_meta.json"
)


@pytest.mark.regression
@pytest.mark.integrations
@allure.epic("Интеграции блогера")
@allure.feature("Выполнение интеграции")
@allure.story("Начать работу, отправить сообщение и загрузить медиа")
@allure.tag("Regression", "Integrations", "Execute")
class TestIntegration01Execute:

    @allure.title("integration-01: works → начать работу → чат → загрузка медиа")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_execute_integration(self, blogger_page: Page):
        page = IntegrationPage(blogger_page)

        # Переходим на страницу интеграций (filter=New)
        with allure.step(f"Открыть {WORKS_URL}"):
            blogger_page.goto(WORKS_URL, wait_until="networkidle")
            blogger_page.wait_for_timeout(3000)

        # Определяем название продукта (из json если есть, иначе первая карточка)
        product_name = self._resolve_product_name(blogger_page)

        # Клик по карточке продукта (с retry)
        page.click_product_card(product_name)

        # Чат с рекламодателем
        page.click_chat_button()
        page.send_chat_message(CHAT_MESSAGE)
        page.wait_for_chat_message(CHAT_MESSAGE)

        # Начать работу
        page.wait(2000)
        page.click_start_work()

        # Загрузка медиа для первых 3 шагов
        page.upload_all_media_steps(count=3)

        # Шаг 4 — Медиа-контент (видео) — без перехода, продолжаем на той же странице
        page.upload_step4_media_and_submit()

    @staticmethod
    def _resolve_product_name(browser_page: Page) -> str:
        """Получить название продукта.

        1) Из last_product_meta.json если файл существует.
        2) Иначе — берём заголовок первой карточки на странице.
        """
        if LAST_PRODUCT_META_PATH.exists():
            meta = json.loads(LAST_PRODUCT_META_PATH.read_text(encoding="utf-8"))
            name = (meta.get("name") or "").strip()
            if name:
                return name

        # Fallback: первая карточка на странице
        first_card = browser_page.locator("span.line-clamp-2").first
        expect(first_card).to_be_visible(timeout=15000)
        return first_card.inner_text().strip()
