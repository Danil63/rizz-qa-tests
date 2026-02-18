"""PCO: Компонент фильтров на странице маркета блогера."""
import allure
from playwright.sync_api import Page, expect

from tests.components.base_component import BaseComponent


class FilterComponent(BaseComponent):
    """Компонент фильтров и поиска на странице /app/creator/market."""

    def __init__(self, page: Page):
        super().__init__(page)

        # ── Локаторы элементов ────────────────────────────────
        self.search_input = page.get_by_role("textbox", name="Поиск")
        self.btn_social = page.get_by_role("button", name="Социальная сеть")
        self.btn_marketplace = page.get_by_role("button", name="Маркетплейс")
        self.btn_category = page.get_by_role("button", name="Категория")
        self.btn_reward = page.get_by_role("button", name="Вознаграждение")
        self.btn_options = page.get_by_role("button", name="Опции кампании")
        self.btn_sort = page.get_by_role("button", name="Сортировка")

    # ── Методы действий ───────────────────────────────────────

    @allure.step('Ввод "{query}" в поле поиска')
    def fill_search(self, query: str) -> None:
        """Ввести текст в поле поиска."""
        self.search_input.click()
        self.search_input.fill(query)

    @allure.step('Очистка поля поиска')
    def clear_search(self) -> None:
        """Стереть текст в поле поиска."""
        self.search_input.click()
        self.search_input.fill("")

    @allure.step('Нажать Enter в поле поиска')
    def press_search_enter(self) -> None:
        """Нажать Enter в поле поиска."""
        self.search_input.press("Enter")

    @allure.step('Выбор в dropdown "{dropdown_name}" значение "{option_name}"')
    def select_dropdown_option(self, dropdown_name: str, option_name: str) -> None:
        """Открыть dropdown по имени кнопки и выбрать опцию."""
        btn = self._get_dropdown_button(dropdown_name)
        btn.click()
        # Опция внутри диалога (Radix popover)
        option = self.page.get_by_role("option", name=option_name)
        option.click()

    @allure.step('Закрытие dropdown "{dropdown_name}"')
    def close_dropdown(self, dropdown_name: str) -> None:
        """Закрыть dropdown повторным кликом."""
        btn = self._get_dropdown_button(dropdown_name)
        btn.click()

    # ── Приватные методы ──────────────────────────────────────

    def _get_dropdown_button(self, name: str):
        """Вернуть локатор кнопки dropdown по имени."""
        mapping = {
            "Социальная сеть": self.btn_social,
            "Маркетплейс": self.btn_marketplace,
            "Категория": self.btn_category,
            "Вознаграждение": self.btn_reward,
            "Опции кампании": self.btn_options,
            "Сортировка": self.btn_sort,
        }
        return mapping[name]

    # ── Методы проверок ───────────────────────────────────────

    @allure.step('Проверка: первая карточка содержит текст "{text}"')
    def check_first_card_contains(self, text: str) -> None:
        """Проверить что заголовок первой карточки содержит текст."""
        first_card = self.page.locator(".rounded-xl.bg-white.p-1").first
        first_title = first_card.locator("h3")
        expect(first_title).to_contain_text(text, ignore_case=True)

    @allure.step('Проверка: карточки отображаются после фильтрации')
    def check_cards_visible(self) -> None:
        """Проверить что хотя бы одна карточка видна."""
        first_card = self.page.locator(".rounded-xl.bg-white.p-1").first
        expect(first_card).to_be_visible(timeout=10000)

    @allure.step('Проверка: в карточках отображается плашка "{badge_text}"')
    def check_badge_visible_in_cards(self, badge_text: str) -> None:
        """Проверить что хотя бы одна карточка содержит указанный бейдж."""
        card_with_badge = self.page.locator(
            f".rounded-xl.bg-white.p-1:has-text('{badge_text}')"
        ).first
        expect(card_with_badge).to_be_visible(timeout=10000)

    @allure.step('Проверка: выдача не изменилась (карточки видны)')
    def check_results_unchanged(self) -> None:
        """Проверить что карточки по-прежнему видны (выдача не сбросилась)."""
        first_card = self.page.locator(".rounded-xl.bg-white.p-1").first
        expect(first_card).to_be_visible(timeout=10000)
