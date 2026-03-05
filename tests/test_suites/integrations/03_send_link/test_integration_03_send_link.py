"""integration-03: Отправка ссылки на публикацию в социальной сети блогером."""

import json
from pathlib import Path

import allure
import pytest
from playwright.sync_api import Page

from tests.pages.integration_page import IntegrationPage

PUBLICATION_LINK = "https://www.instagram.com/p/test_publication_link/"
INTEGRATIONS_PATH = (
    Path(__file__).resolve().parents[3] / "test_data" / "integrations.json"
)


@pytest.mark.regression
@pytest.mark.integrations
@allure.epic("Интеграции блогера")
@allure.feature("Отправка ссылки на публикацию")
@allure.story("Отправить ссылку на размещение в социальной сети")
@allure.tag("Regression", "Integrations", "SendLink", "SocialNetwork")
class TestIntegration03SendLink:
    @allure.title("integration-03: works → карточка → отправить ссылку на публикацию")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_send_publication_link(self, blogger_page: Page):
        page = IntegrationPage(blogger_page)

        # Шаг 1: открыть сохранённую страницу интеграции блогера
        creator_url = self._get_creator_url()
        with allure.step(f"Открыть страницу интеграции: {creator_url}"):
            blogger_page.goto(creator_url, wait_until="networkidle")
            blogger_page.wait_for_timeout(2_000)

        # Шаг 2: отправить ссылку на публикацию в «Размещение в социальной сети»
        page.submit_publication_link_with_retry(
            url=PUBLICATION_LINK,
            max_retries=3,
            wait_timeout_ms=5_000,
        )

    @staticmethod
    def _get_creator_url() -> str:
        """Получить URL интеграции блогера из integrations.json."""
        if not INTEGRATIONS_PATH.exists():
            raise AssertionError(
                "integrations.json не найден. Сначала запустите test_integration_01_execute.py"
            )
        data = json.loads(INTEGRATIONS_PATH.read_text(encoding="utf-8"))
        url = (data.get("creator") or "").strip()
        if not url:
            raise AssertionError(
                "creator URL не найден в integrations.json. "
                "Сначала запустите test_integration_01_execute.py"
            )
        return url
