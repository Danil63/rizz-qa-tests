"""edit-fix-comp: Редактирование кампании с Фиксированной оплатой."""

import json
import random
from pathlib import Path

import pytest
from faker import Faker
from playwright.sync_api import Page, expect

from tests.pages.campaign_details_page import CampaignDetailsPage
from tests.pages.campaigns_page import CampaignsPage
from tests.pages.edit_campaign_page import EditCampaignPage
from tests.test_data.campaign_generator import THEMATICS

fake = Faker("ru_RU")

FIX_CAMPAIGN_CONTEXT_PATH = (
    Path(__file__).resolve().parents[3] / "test_data" / "fix_campaing_context.json"
)


@pytest.mark.regression
@pytest.mark.campaigns
class TestEditFixCamp:

    def test_edit_fix_camp(self, campaigns_page: CampaignsPage, page: Page):
        assert FIX_CAMPAIGN_CONTEXT_PATH.exists(), (
            f"Файл с контекстом кампании не найден: {FIX_CAMPAIGN_CONTEXT_PATH}. "
            "Сначала запусти test_campaigns_03_create.py"
        )
        ctx = json.loads(FIX_CAMPAIGN_CONTEXT_PATH.read_text(encoding="utf-8"))
        campaign_title = (ctx.get("campaign_title") or "").strip()
        assert campaign_title, "Поле campaign_title в fix_campaing_context.json пустое"

        # Шаг 1: переключиться на таб «Активные»
        campaigns_page.switch_tab("Активные")
        page.wait_for_timeout(1_500)

        # Шаг 2: кликнуть по заголовку кампании
        details_page = CampaignDetailsPage(page)
        details_page.click_campaign_title(campaign_title)

        # Шаг 3: проверить якорь «Детали кампании» (таймаут 5 сек)
        expect(details_page.details_heading).to_be_visible(timeout=5_000)

        # Шаг 4: нажать кнопку «Редактировать»
        details_page.click_edit_button()

        # Шаг 5: проверить заголовок страницы редактирования
        edit_page = EditCampaignPage(page)
        expect(edit_page.heading).to_be_visible(timeout=10_000)

        # Шаг 6: обновить название + сохранить в JSON
        new_name = f"Тестовая кампания — {fake.catch_phrase()}"
        edit_page.update_name(new_name)

        ctx["campaign_title"] = new_name
        FIX_CAMPAIGN_CONTEXT_PATH.write_text(
            json.dumps(ctx, ensure_ascii=False, indent=2), encoding="utf-8"
        )

        # Шаг 7: выбрать новую соц. сеть «VK»
        edit_page.select_vk_format()

        # Шаг 8: добавить 2 новые тематики
        new_thematics = random.sample(THEMATICS, 2)
        for thematic in new_thematics:
            edit_page.add_thematic(thematic)

        # Шаг 9: увеличить «Вознаграждение за 1 интеграцию» на 5
        edit_page.increase_fix_reward(5)

        # Шаг 10: сохранить
        edit_page.click_save()

        # Шаг 11: проверить возврат на страницу деталей кампании
        expect(details_page.details_heading).to_be_visible(timeout=10_000)
