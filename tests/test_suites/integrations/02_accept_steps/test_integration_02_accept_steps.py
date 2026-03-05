"""integration-02: Принятие шагов интеграции рекламодателем + проверка чата."""

import json
from pathlib import Path

import allure
import pytest
from playwright.sync_api import Page
from tests.pages.integration_page import IntegrationPage

EXPECTED_MESSAGE = "Приступаю к выполнению работы"
REPLY_MESSAGE = "Хорошо, мне все понравилось!"
INTEGRATIONS_PATH = (
    Path(__file__).resolve().parents[3] / "test_data" / "integrations.json"
)


@pytest.mark.regression
@pytest.mark.integrations
@allure.epic("Интеграции рекламодателя")
@allure.feature("Принятие шагов интеграции")
@allure.story("Принять 4 шага, проверить чат, отправить сообщение")
@allure.tag("Regression", "Integrations", "AcceptSteps")
class TestIntegration02AcceptSteps:
    @allure.title(
        "integration-02: интеграция рекламодателя → принять 4 шага → чат → сообщение"
    )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_accept_steps_and_chat(self, advertiser_page: Page):
        page = IntegrationPage(advertiser_page)

        # Открыть сохранённую страницу интеграции рекламодателя напрямую
        advertiser_url = self._get_advertiser_url()
        with allure.step(f"Открыть страницу интеграции: {advertiser_url}"):
            advertiser_page.goto(advertiser_url, wait_until="networkidle")
            advertiser_page.wait_for_timeout(2_000)

        # Шаг 1: принять все 4 шага (retry если кнопка не исчезла)
        page.accept_all_steps(max_retries=5)

        # Шаг 2: открыть чат с блогером
        page.open_advertiser_chat()

        # Шаг 3: проверить сообщение блогера
        page.wait_for_chat_message(EXPECTED_MESSAGE)

        # Шаг 4: отправить ответ
        page.send_advertiser_message(REPLY_MESSAGE)

        # Шаг 5: неявное ожидание
        advertiser_page.wait_for_timeout(2_000)

        # Шаг 6: проверить отправленное сообщение
        page.wait_for_chat_message(REPLY_MESSAGE)

    @staticmethod
    def _get_advertiser_url() -> str:
        """Получить URL интеграции рекламодателя из integrations.json."""
        if not INTEGRATIONS_PATH.exists():
            raise AssertionError(
                "integrations.json не найден. Сначала запустите test_integration_01_execute.py"
            )
        data = json.loads(INTEGRATIONS_PATH.read_text(encoding="utf-8"))
        url = (data.get("advertiser") or "").strip()
        if not url:
            raise AssertionError(
                "advertiser URL не найден в integrations.json. "
                "Сначала запустите test_campaigns_02_create.py и test_integration_01_execute.py"
            )
        return url
