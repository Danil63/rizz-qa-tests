"""integration-06-fix: Запуск выплаты и ожидание кнопки подписания акта (fix-кампания)."""

import json
from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

FIX_INTEGRATIONS_PATH = (
    Path(__file__).resolve().parents[3] / "test_data" / "fix_integrations.json"
)


@pytest.mark.regression
@pytest.mark.integrations
class TestIntegration06FixSigningAct:
    def test_signing_act(self, blogger_page: Page):
        creator_url = self._get_creator_url()
        blogger_page.goto(creator_url, wait_until="load", timeout=60_000)
        blogger_page.wait_for_load_state("networkidle", timeout=30_000)
        blogger_page.wait_for_timeout(2_000)

        blogger_page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        blogger_page.wait_for_timeout(1_000)

        start_payout_btn = blogger_page.get_by_role("button", name="Запустить выплату", exact=True)
        expect(start_payout_btn).to_be_visible(timeout=10_000)
        expect(start_payout_btn).to_be_enabled(timeout=5_000)
        start_payout_btn.click()

        sign_btn = blogger_page.get_by_role("button", name="Подписать", exact=True)
        expect(sign_btn).to_be_attached(timeout=15_000)

    @staticmethod
    def _get_creator_url() -> str:
        """Получить URL интеграции блогера из fix_integrations.json."""
        if not FIX_INTEGRATIONS_PATH.exists():
            raise AssertionError(
                "fix_integrations.json не найден. Сначала запустите test_integration_02_fix.py"
            )
        data = json.loads(FIX_INTEGRATIONS_PATH.read_text(encoding="utf-8"))
        url = (data.get("creator") or "").strip()
        if not url:
            raise AssertionError(
                "creator URL не найден в fix_integrations.json. "
                "Сначала запустите test_integration_02_fix.py"
            )
        return url
