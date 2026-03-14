"""integration-04-fix: Принятие шага «Размещение в социальной сети» рекламодателем (fix-кампания)."""

import json
from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

FIX_INTEGRATIONS_PATH = (
    Path(__file__).resolve().parents[3] / "test_data" / "fix_integrations.json"
)


@pytest.mark.regression
@pytest.mark.integrations
class TestIntegration04FixAcceptSocialLink:
    def test_accept_social_link_step(self, advertiser_page: Page):
        advertiser_url = self._get_advertiser_url()
        advertiser_page.goto(advertiser_url, wait_until="networkidle")
        advertiser_page.wait_for_timeout(2_000)

        section = advertiser_page.locator(
            "div.rounded-lg.border.bg-card",
            has=advertiser_page.locator("h3", has_text="Размещение в социальной сети"),
        ).first
        expect(section).to_be_visible(timeout=10_000)
        section.scroll_into_view_if_needed()

        accept_btn = section.get_by_role("button", name="Принять", exact=True)
        expect(accept_btn).to_be_visible(timeout=10_000)
        expect(accept_btn).to_be_enabled(timeout=5_000)
        accept_btn.click()

        expect(accept_btn).not_to_be_visible(timeout=10_000)

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
