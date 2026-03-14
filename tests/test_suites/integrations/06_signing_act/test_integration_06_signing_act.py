"""integration-06: Запуск выплаты и подписание акта выполненных работ блогером."""

import json
from pathlib import Path

import pytest
from playwright.sync_api import Page

from tests.pages.integration_page import IntegrationPage

INTEGRATIONS_PATH = (
    Path(__file__).resolve().parents[3] / "test_data" / "integrations.json"
)


@pytest.mark.regression
@pytest.mark.integrations
class TestIntegration06SigningAct:
    def test_signing_act(self, blogger_page: Page):
        page = IntegrationPage(blogger_page)

        # Шаг 1: открыть сохранённую страницу интеграции блогера
        creator_url = self._get_creator_url()
        blogger_page.goto(creator_url, wait_until="load", timeout=60_000)
        blogger_page.wait_for_load_state("networkidle", timeout=30_000)
        blogger_page.wait_for_timeout(2_000)

        # Шаг 2: проверить что открылась страница интеграции
        page.expect_integration_page()

        # Шаг 3: проскроллить к блоку «Выплата бартерного вознаграждения»
        page.scroll_to_payout_step()

        # Шаг 4: нажать «Запустить выплату» + проверить DOM до и после
        page.click_start_payout()

        # Шаг 5: дождаться появления кнопки «Подписать»
        page.wait_for_sign_button()

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
