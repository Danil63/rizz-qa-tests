"""integration-04: Принятие шага «Размещение в социальной сети» рекламодателем."""

import json
from pathlib import Path

import allure
import pytest
from playwright.sync_api import Page

from tests.pages.integration_page import IntegrationPage

INTEGRATIONS_PATH = (
    Path(__file__).resolve().parents[3] / "test_data" / "integrations.json"
)


@pytest.mark.regression
@pytest.mark.integrations
@allure.epic("Интеграции рекламодателя")
@allure.feature("Принятие шагов интеграции")
@allure.story("Принять шаг «Размещение в социальной сети» и проверить смену статуса")
@allure.tag("Regression", "Integrations", "AcceptSteps", "SocialLink")
class TestIntegration03AcceptSocialLink:
    @allure.title("integration-04: принять шаг «Размещение в социальной сети»")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_accept_social_link_step(self, advertiser_page: Page):
        page = IntegrationPage(advertiser_page)

        # Шаг 1: открыть сохранённую страницу интеграции рекламодателя
        advertiser_url = self._get_advertiser_url()
        with allure.step(f"Открыть страницу интеграции: {advertiser_url}"):
            advertiser_page.goto(advertiser_url, wait_until="networkidle")
            advertiser_page.wait_for_timeout(2_000)

        # Шаг 2: скроллить к блоку и нажать «Принять» (retry по статус-бейджу)
        page.accept_publication_link_with_retry(max_retries=3, wait_timeout_ms=5_000)

        # Шаг 3: финальная проверка — бейдж «Принят» + кнопки исчезли
        page.check_publication_link_accepted()

    @staticmethod
    def _get_advertiser_url() -> str:
        """Получить URL интеграции рекламодателя из integrations.json."""
        if not INTEGRATIONS_PATH.exists():
            raise AssertionError(
                "integrations.json не найден. Сначала запустите test_integration_02_accept_steps.py"
            )
        data = json.loads(INTEGRATIONS_PATH.read_text(encoding="utf-8"))
        url = (data.get("advertiser") or "").strip()
        if not url:
            raise AssertionError(
                "advertiser URL не найден в integrations.json. "
                "Сначала запустите test_integration_02_accept_steps.py"
            )
        return url
