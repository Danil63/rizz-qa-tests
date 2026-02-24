"""POM: Страница редактирования рекламной кампании."""
import allure
from playwright.sync_api import Page, expect

from tests.pages.base_page import BasePage


class EditCampaignPage(BasePage):
    """Page Object для /app/advertiser/campaigns/<id>/edit."""

    def __init__(self, page: Page):
        super().__init__(page)

        # ── Заголовок ─────────────────────────────────────────
        self.heading = page.get_by_role("heading", name="Редактировать рекламную кампанию")

        # ── Поля формы ────────────────────────────────────────
        self.input_name = page.get_by_role("textbox", name="Название")
        self.input_task = page.get_by_role("textbox", name="Задание")
        self.input_link = page.get_by_role("textbox", name="Cсылка на товар")
        self.input_integrations = page.get_by_role("textbox", name="Количество интеграций")
        self.input_max_reward = page.get_by_role("textbox", name="Максимальное вознаграждение")

        # ── Кнопка сохранения ─────────────────────────────────
        self.btn_save = page.get_by_role("button", name="Сохранить")

    # ── Методы действий ───────────────────────────────────────

    @allure.step("Проверка: страница редактирования загружена")
    def expect_loaded(self) -> None:
        """Проверить что страница редактирования загружена."""
        self.expect_url_contains(r".*/edit")
        expect(self.heading).to_be_visible()

    @allure.step('Обновление названия кампании: "{value}"')
    def update_name(self, value: str) -> None:
        """Очистить и заполнить поле Название."""
        self.input_name.click()
        self.input_name.clear()
        self.input_name.fill(value)

    @allure.step("Обновление задания")
    def update_task(self, value: str) -> None:
        """Очистить и заполнить поле Задание."""
        self.input_task.click()
        self.input_task.clear()
        self.input_task.fill(value)

    @allure.step('Увеличение вознаграждения на {delta} ₽')
    def increase_reward(self, delta: int) -> None:
        """Прочитать текущее вознаграждение, увеличить на delta."""
        current = self.input_max_reward.input_value().strip().replace(" ", "")
        new_value = str(int(current) + delta)
        self.input_max_reward.click()
        self.input_max_reward.clear()
        self.input_max_reward.fill(new_value)

    @allure.step('Нажатие кнопки "Сохранить"')
    def click_save(self) -> None:
        """Нажать кнопку Сохранить."""
        self.btn_save.click()
