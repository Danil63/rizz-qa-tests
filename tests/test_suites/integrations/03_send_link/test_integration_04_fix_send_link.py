"""integration-03-fix: Отправка ссылки на публикацию блогером (fix-кампания)."""

import json
from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

PUBLICATION_LINK = "https://www.tiktok.com/@ann.malevichh/video/7613853951523376406"
FIX_INTEGRATIONS_PATH = (
    Path(__file__).resolve().parents[3] / "test_data" / "fix_integrations.json"
)


@pytest.mark.regression
@pytest.mark.integrations
class TestIntegration03FixSendLink:
    def test_send_publication_link(self, blogger_page: Page):
        creator_url = self._get_creator_url()
        blogger_page.goto(creator_url, wait_until="networkidle")
        blogger_page.wait_for_timeout(2_000)

        section = blogger_page.locator("#step-3")
        expect(section).to_be_visible(timeout=10_000)
        section.scroll_into_view_if_needed()

        input_field = blogger_page.locator("#step-3 input[name='value']")
        expect(input_field).to_be_visible(timeout=10_000)
        input_field.fill(PUBLICATION_LINK)

        submit_btn = blogger_page.locator("#step-3 button[type='submit']")
        expect(submit_btn).to_be_visible(timeout=10_000)
        expect(submit_btn).to_be_enabled(timeout=5_000)
        submit_btn.click()

        expect(submit_btn).not_to_be_visible(timeout=10_000)

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
