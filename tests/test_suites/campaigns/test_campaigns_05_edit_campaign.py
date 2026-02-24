"""campaigns-05: Редактирование рекламной кампании.

Сценарий:
    1) Открыть /app/advertiser/campaigns
    2) Проверить, что таб «Активные» выбран по умолчанию
    3) Найти кампанию по названию из last_campaign_title.txt
    4) Нажать на заголовок кампании
    5) Нажать «Редактировать»
    6) Обновить Название, Задание, увеличить стоимость на 2 ₽
    7) Нажать «Сохранить»
    8) Подождать 2 секунды
"""
import time
from pathlib import Path

import allure
import pytest
from faker import Faker
from playwright.sync_api import Page, expect

from tests.pages.campaigns_page import CampaignsPage
from tests.pages.edit_campaign_page import EditCampaignPage

fake = Faker("ru_RU")

LAST_CAMPAIGN_TITLE_PATH = Path(__file__).resolve().parents[2] / "test_data" / "last_campaign_title.txt"


@pytest.mark.regression
@pytest.mark.campaigns
@allure.epic("Кампании рекламодателя")
@allure.feature("Редактирование кампании")
@allure.story("Обновление названия, задания и стоимости")
@allure.tag("Regression", "Campaigns", "Edit")
class TestCampaigns05:
    """campaigns-05: Редактирование кампании — обновить название, задание, стоимость +2₽."""

    @allure.title("campaigns-05: Найти кампанию → Редактировать → обновить данные → Сохранить")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_campaigns_05_edit_campaign(
        self,
        campaigns_page: CampaignsPage,
        page: Page,
    ):
        assert LAST_CAMPAIGN_TITLE_PATH.exists(), (
            f"Файл с заголовком не найден: {LAST_CAMPAIGN_TITLE_PATH}. "
            "Сначала запусти тест создания кампании campaigns-02."
        )
        old_title = LAST_CAMPAIGN_TITLE_PATH.read_text(encoding="utf-8").strip()
        assert old_title, "Файл last_campaign_title.txt пустой"

        # 1-2) Страница кампаний, таб «Активные» выбран
        campaigns_page.check_active_tab_selected()

        # 3) Найти кампанию по названию
        campaign_link = page.locator("main").locator(f"text='{old_title}'").first
        expect(campaign_link).to_be_visible(timeout=10000)

        # 4) Нажать на заголовок кампании
        campaign_link.click()
        page.wait_for_timeout(1500)

        # 5) Нажать «Редактировать»
        edit_button = page.get_by_role("link", name="Редактировать")
        expect(edit_button).to_be_visible()
        edit_button.click()

        # Проверяем переход на страницу редактирования
        edit_page = EditCampaignPage(page)
        edit_page.expect_loaded()

        # 6) Генерируем новые данные
        new_title = f"Тестовая кампания — {fake.catch_phrase()}"
        new_task = (
            f"Обновлённое задание: снять обзор товара в формате Reels.\n\n"
            f"1. Найти товар по ключевому запросу «{fake.word()}» на маркетплейсе.\n"
            f"2. Сделать распаковку и показать товар в использовании.\n"
            f"3. Оставить отзыв с фото, 5 ⭐.\n\n"
            f"Комментарий: {fake.sentence()}"
        )

        # Обновляем название
        edit_page.update_name(new_title)

        # Обновляем задание
        edit_page.update_task(new_task)

        # Увеличиваем стоимость на 2 ₽
        edit_page.increase_reward(2)

        allure.attach(
            f"Старое название: {old_title}\n"
            f"Новое название: {new_title}\n"
            f"Новое задание: {new_task}\n"
            f"Стоимость: +2 ₽",
            name="Данные редактирования",
            attachment_type=allure.attachment_type.TEXT,
        )

        # 7) Сохранить
        edit_page.click_save()

        # Обновляем файл с названием кампании
        LAST_CAMPAIGN_TITLE_PATH.write_text(new_title, encoding="utf-8")

        # 8) Задержка 2 секунды
        time.sleep(2)
