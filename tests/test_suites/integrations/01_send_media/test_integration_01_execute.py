"""integration-01: Выполнение интеграции блогером."""
import json
from pathlib import Path

import allure
import pytest
from playwright.sync_api import Page

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
        # Определяем название продукта
        product_name = self._resolve_product_name()

        page = IntegrationPage(blogger_page)

        # Переходим на страницу интеграций (filter=New)
        blogger_page.goto(WORKS_URL, wait_until="networkidle")

        # Клик по карточке продукта (с retry)
        page.click_product_card(product_name)

        # Чат с рекламодателем
        page.click_chat_button()
        page.send_chat_message(CHAT_MESSAGE)
        page.wait_for_chat_message(CHAT_MESSAGE)

        # Начать работу
        page.wait(2000)
        page.click_start_work()

        # Загрузка медиа для 4 шагов
        page.upload_all_media_steps(count=4)

    @staticmethod
    def _resolve_product_name() -> str:
        """Получить название продукта из last_product_meta.json."""
        assert LAST_PRODUCT_META_PATH.exists(), (
            f"Файл {LAST_PRODUCT_META_PATH} не найден. "
            "Сначала запусти тест создания продукта."
        )
        meta = json.loads(LAST_PRODUCT_META_PATH.read_text(encoding="utf-8"))
        product_name = (meta.get("name") or "").strip()
        assert product_name, "Поле name в last_product_meta.json пустое"
        return product_name
