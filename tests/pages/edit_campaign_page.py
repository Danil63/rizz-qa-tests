"""POM: Страница редактирования рекламной кампании."""

from playwright.sync_api import Page, expect

from tests.pages.base_page import BasePage


class EditCampaignPage(BasePage):
    """Page Object для /app/advertiser/campaigns/<id>/edit."""

    def __init__(self, page: Page):
        super().__init__(page)

        # ── Заголовок ─────────────────────────────────────────
        self.heading = page.get_by_role(
            "heading", name="Редактировать рекламную кампанию"
        )

        # ── Поля формы ────────────────────────────────────────
        self.input_name = page.get_by_role("textbox", name="Название")
        self.input_task = page.get_by_role("textbox", name="Задание")
        self.input_link = page.get_by_role("textbox", name="Cсылка на товар")
        self.input_integrations = page.get_by_role(
            "textbox", name="Количество интеграций"
        )
        self.input_max_reward = page.get_by_role(
            "textbox", name="Максимальное вознаграждение"
        )

        # ── Вознаграждение (Фиксированная) ────────────────────
        self.input_fix_reward = page.get_by_role(
            "textbox", name="Вознаграждение за 1 интеграцию"
        )

        # ── Формат контента: кнопка "Добавить" ────────────────
        self._btn_format_add = page.get_by_role("button", name="Добавить").first

        # ── VK-чекбоксы (в диалоге формата контента) ──────────
        self.checkbox_vk_clip = page.get_by_role("checkbox", name="Клип")
        self.checkbox_vk_post = page.get_by_role("checkbox", name="Пост").last

        # ── Тематика: кнопка "Добавить" ───────────────────────
        self.btn_thematic_add = page.get_by_role("button", name="Добавить").last

        # ── Кнопка сохранения ─────────────────────────────────
        self.btn_save = page.get_by_role("button", name="Сохранить")

    # ── Методы действий ───────────────────────────────────────

    def expect_loaded(self) -> None:
        """Проверить что страница редактирования загружена."""
        self.expect_url_contains(r".*/edit")
        expect(self.heading).to_be_visible()

    def update_name(self, value: str) -> None:
        """Очистить и заполнить поле Название."""
        self.input_name.click()
        self.input_name.clear()
        self.input_name.fill(value)

    def update_task(self, value: str) -> None:
        """Очистить и заполнить поле Задание."""
        self.input_task.click()
        self.input_task.clear()
        self.input_task.fill(value)

    def increase_reward(self, delta: int) -> None:
        """Прочитать текущее вознаграждение, увеличить на delta."""
        current = self.input_max_reward.input_value().strip().replace(" ", "")
        new_value = str(int(current) + delta)
        self.input_max_reward.click()
        self.input_max_reward.clear()
        self.input_max_reward.fill(new_value)

    def select_vk_format(self) -> None:
        """Открыть диалог формата контента и выбрать VK Клип."""
        self._btn_format_add.click()
        self.page.wait_for_timeout(300)
        if not self.checkbox_vk_clip.is_checked():
            self.checkbox_vk_clip.click()
        self.page.keyboard.press("Escape")

    def add_thematic(self, option_name: str) -> None:
        """Открыть диалог тематики и выбрать новую опцию."""
        self.btn_thematic_add.click()
        self.page.wait_for_timeout(500)
        self.page.get_by_role("option", name=option_name, exact=True).click()
        self.page.keyboard.press("Escape")

    def increase_fix_reward(self, delta: int) -> None:
        """Прочитать текущее значение поля fix-вознаграждения, увеличить на delta."""
        current = self.input_fix_reward.input_value().strip().replace(" ", "")
        new_value = str(int(current) + delta)
        self.input_fix_reward.click()
        self.input_fix_reward.clear()
        self.input_fix_reward.fill(new_value)

    def click_save(self) -> None:
        """Нажать кнопку Сохранить."""
        self.btn_save.click()
