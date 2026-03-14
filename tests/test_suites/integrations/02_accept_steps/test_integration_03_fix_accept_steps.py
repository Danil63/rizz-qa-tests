"""integration-02-fix: Принятие шагов интеграции рекламодателем (fix-кампания)."""

import json
from pathlib import Path

import pytest
from playwright.sync_api import Page

from tests.pages.integration_page import IntegrationPage

FIX_INTEGRATIONS_PATH = (
    Path(__file__).resolve().parents[3] / "test_data" / "fix_integrations.json"
)


@pytest.mark.regression
@pytest.mark.integrations
class TestIntegration02FixAcceptSteps:
    def test_accept_fix_steps(self, advertiser_page: Page):
        page = IntegrationPage(advertiser_page)

        advertiser_url = self._get_advertiser_url()
        advertiser_page.goto(advertiser_url, wait_until="networkidle")
        advertiser_page.wait_for_timeout(2_000)

        page.accept_all_steps(max_retries=5)

    @staticmethod
    def _get_advertiser_url() -> str:
        """Получить advertiser URL интеграции из fix_integrations.json."""
        if not FIX_INTEGRATIONS_PATH.exists():
            raise AssertionError(
                "fix_integrations.json не найден. Сначала запустите test_integration_02_fix.py"
            )
        data = json.loads(FIX_INTEGRATIONS_PATH.read_text(encoding="utf-8"))
        url = (data.get("advertiser") or "").strip()
        if not url:
            raise AssertionError(
                "advertiser URL не найден в fix_integrations.json. "
                "Сначала запустите test_integration_02_fix.py"
            )
        return url
