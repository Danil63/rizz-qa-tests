"""POM: Страница создания рекламной кампании."""
import allure
from playwright.sync_api import Page, expect

from tests.pages.base_page import BasePage


class CreateCampaignPage(BasePage):
    """Page Object для https://app.rizz.market/app/advertiser/campaigns/create."""

    URL = "https://app.rizz.market/app/advertiser/campaigns/create"

    def __init__(self, page: Page):
        super().__init__(page)

        # ── Хлебные крошки ────────────────────────────────────
        self.breadcrumb = page.get_by_role("navigation", name="breadcrumb")
        self.breadcrumb_campaigns = self.breadcrumb.get_by_role("link", name="Кампании")
        self.breadcrumb_create = self.breadcrumb.get_by_role("link", name="Создание")

        # ── Заголовок ─────────────────────────────────────────
        self.heading = page.get_by_role("heading", name="Новая рекламная кампания")

        # ── Поле: Название ────────────────────────────────────
        self.input_name = page.get_by_role("textbox", name="Название")
        self.hint_name = page.get_by_text(
            "Название непубличное, назовите для своего удобства в списке кампаний"
        )

        # ── Поле: Предмет рекламы (combobox → dialog) ────────
        self.select_product = page.get_by_role("combobox", name="Выберите предмет рекламы")
        self.product_search_input = page.get_by_role("textbox", name="Поиск")
        self.product_suggestions = page.get_by_role("listbox", name="Suggestions")

        # ── Поле: Ссылка с UTM ────────────────────────────────
        self.input_utm_link = page.get_by_role("textbox", name="Ссылка с UTM")

        # ── Поле: Формат контента (кнопка → dialog) ──────────
        self.content_format_label = page.get_by_text("Формат контента", exact=True)
        self.btn_content_format = page.locator(
            "generic:has-text('Формат контента') >> button:has-text('Добавить')"
        )
        # Fallback: кнопка "Добавить" рядом с "Формат контента"
        self._btn_format_add = page.get_by_role("button", name="Добавить").first

        # Чекбоксы форматов Ig (в dialog)
        self.checkbox_ig_story = page.get_by_role("checkbox", name="История")
        self.checkbox_ig_post = page.get_by_role("checkbox", name="Пост").first
        self.checkbox_ig_reels = page.get_by_role("checkbox", name="Reels")

        # Чекбоксы форматов Youtube
        self.checkbox_yt_shorts = page.get_by_role("checkbox", name="Shorts")
        self.checkbox_yt_video = page.get_by_role("checkbox", name="Видео").first
        self.checkbox_yt_post = page.get_by_role("checkbox", name="Пост").nth(1)

        # Чекбоксы форматов TikTok
        self.checkbox_tt_video = page.get_by_role("checkbox", name="Видео").nth(1)

        # Чекбоксы форматов VK
        self.checkbox_vk_clip = page.get_by_role("checkbox", name="Клип")
        self.checkbox_vk_post = page.get_by_role("checkbox", name="Пост").last

        # ── Информационный блок о законе Ig ──────────────────
        self.ig_law_warning = page.get_by_text("С 1 сентября вступает закон")
        self.ig_law_details_link = page.get_by_role("link", name="Подробнее")

        # ── Поле: Тематика (кнопка → dialog с combobox) ──────
        self.thematic_label = page.get_by_text("Тематика", exact=True)
        self.btn_thematic_add = page.get_by_role("button", name="Добавить").last
        self.thematic_suggestions = page.get_by_role("listbox", name="Suggestions")

        # ── Поле: Задание ─────────────────────────────────────
        self.task_label_simple = page.get_by_text("Простой", exact=True)
        self.task_label_extended = page.get_by_text("Расширенный", exact=True)
        self.task_mode_switch = page.get_by_role("switch").first
        self.input_task = page.get_by_role("textbox", name="Задание")

        # ── Секция: Расчет оплаты ─────────────────────────────
        self.heading_payment = page.get_by_role("heading", name="Расчет оплаты")

        # Тип оплаты (табы)
        self.tab_barter = page.get_by_role("tab", name="Бартер")
        self.tab_fixed = page.get_by_role("tab", name="Фиксированная")
        self.tab_per_views = page.get_by_role("tab", name="За просмотры")

        # Поля Бартер
        self.input_max_compensation = page.get_by_role(
            "textbox", name="Максимальная компенсация за товар"
        )
        self.input_integrations_count = page.get_by_role(
            "textbox", name="Кол-во интеграций"
        )

        # Switch: Автоодобрение откликов
        self.switch_auto_approve = page.get_by_role("switch", name="Автоодобрение откликов")

        # Минимальный охват блогера
        self.input_min_coverage = page.get_by_role(
            "textbox", name="Минимальный охват блогера"
        )

        # Детализация стоимости
        self.btn_cost_details = page.get_by_role(
            "button", name="Показать детализацию стоимости"
        )

        # ── Кнопка создания ───────────────────────────────────
        self.btn_create_campaign = page.get_by_role("button", name="Создать кампанию")

        # ── Cookie-диалог ─────────────────────────────────────
        self.cookie_accept = page.get_by_role("button", name="Принять cookie")

        # ── Уведомление Telegram ──────────────────────────────
        self.telegram_notification = page.get_by_text(
            "Подключите уведомления в Telegram"
        )

        # ── Ошибки валидации (p.text-sm.text-red-700) ─────────
        self.all_errors = page.locator("p.text-sm.text-red-700")

        # Название → "Обязательное поле"
        self.error_name = page.get_by_role("textbox", name="Название").locator(
            ".. >> p.text-red-700"
        )

        # Предмет рекламы → "Обязательное поле"
        self.error_product = page.locator(
            "text=Выберите предмет рекламы >> .. >> p.text-red-700"
        )

        # Формат контента → "Необходимо выбрать социальную сеть"
        self.error_content_format = page.locator(
            "text=Формат контента >> .. >> p.text-red-700"
        )

        # Тематика → "Нужно выбрать хотя бы одну тематику."
        self.error_thematic = page.locator(
            "text=Тематика >> .. >> p.text-red-700"
        )

        # Задание → "Значение слишком маленькое. Минимум: 5"
        self.error_task = page.get_by_role("textbox", name="Задание").locator(
            ".. >> p.text-red-700"
        )

    # ── Методы действий ───────────────────────────────────────

    @allure.step("Принять cookie")
    def accept_cookies(self) -> None:
        """Принять cookie, если диалог отображается."""
        if self.cookie_accept.is_visible(timeout=3000):
            self.cookie_accept.click()

    @allure.step("Закрыть уведомление Telegram")
    def close_telegram_notification(self) -> None:
        """Закрыть баннер Telegram-уведомлений, если виден."""
        close_btn = self.page.locator(
            "button:near(:text('Подключите уведомления в Telegram'))"
        ).last
        if self.telegram_notification.is_visible(timeout=2000):
            close_btn.click()

    @allure.step('Ввод названия кампании: "{value}"')
    def fill_name(self, value: str) -> None:
        """Заполнить поле Название."""
        self.input_name.click()
        self.input_name.fill(value)

    @allure.step('Выбор предмета рекламы по поиску: "{search_text}"')
    def select_product_by_search(self, search_text: str) -> None:
        """Открыть combobox, ввести поиск, выбрать первый результат."""
        self.select_product.click()
        self.page.wait_for_timeout(500)
        self.product_search_input.fill(search_text)
        self.page.wait_for_timeout(1000)
        # Выбираем первый option из результатов
        first_option = self.product_suggestions.get_by_role("option").first
        first_option.click()

    @allure.step('Ввод ссылки с UTM: "{value}"')
    def fill_utm_link(self, value: str) -> None:
        """Заполнить поле Ссылка с UTM."""
        self.input_utm_link.click()
        self.input_utm_link.fill(value)

    @allure.step("Открыть диалог формата контента")
    def open_content_format_dialog(self) -> None:
        """Нажать кнопку Добавить для формата контента."""
        self._btn_format_add.click()
        self.page.wait_for_timeout(300)

    @allure.step("Выбрать все 3 формата Ig (История, Пост, Reels)")
    def select_ig_all_formats(self) -> None:
        """Отметить все 3 чекбокса Ig: История, Пост, Reels."""
        self.open_content_format_dialog()
        if not self.checkbox_ig_story.is_checked():
            self.checkbox_ig_story.click()
        if not self.checkbox_ig_post.is_checked():
            self.checkbox_ig_post.click()
        if not self.checkbox_ig_reels.is_checked():
            self.checkbox_ig_reels.click()
        # Закрыть диалог кликом вне
        self.page.keyboard.press("Escape")

    @allure.step('Выбор тематики: "{option_name}"')
    def select_thematic(self, option_name: str) -> None:
        """Открыть диалог тематики и выбрать опцию."""
        self.btn_thematic_add.click()
        self.page.wait_for_timeout(500)
        self.page.get_by_role("option", name=option_name, exact=True).click()
        self.page.keyboard.press("Escape")

    @allure.step('Ввод задания')
    def fill_task(self, value: str) -> None:
        """Заполнить поле Задание."""
        self.input_task.click()
        self.input_task.fill(value)

    @allure.step('Ввод максимальной компенсации: "{value}"')
    def fill_max_compensation(self, value: str) -> None:
        """Заполнить поле Максимальная компенсация за товар."""
        self.input_max_compensation.click()
        self.input_max_compensation.clear()
        self.input_max_compensation.fill(value)

    @allure.step("Переключить Автоодобрение откликов (выключить)")
    def toggle_auto_approve_off(self) -> None:
        """Выключить switch Автоодобрение откликов (из checked → unchecked)."""
        if self.switch_auto_approve.is_checked():
            self.switch_auto_approve.click()

    @allure.step("Переключить Автоодобрение откликов (включить)")
    def toggle_auto_approve_on(self) -> None:
        """Включить switch Автоодобрение откликов."""
        if not self.switch_auto_approve.is_checked():
            self.switch_auto_approve.click()

    @allure.step('Нажатие кнопки "Создать кампанию"')
    def click_create_campaign(self) -> None:
        """Нажать кнопку Создать кампанию."""
        self.btn_create_campaign.click()

    @allure.step("Заполнение всех полей формы создания кампании")
    def fill_all_fields(
        self,
        name: str,
        product_search: str,
        utm_link: str,
        thematic: str,
        task: str,
        max_compensation: str,
    ) -> None:
        """Заполнить все поля формы создания кампании."""
        self.fill_name(name)
        self.select_product_by_search(product_search)
        self.fill_utm_link(utm_link)
        self.select_ig_all_formats()
        self.select_thematic(thematic)
        self.fill_task(task)
        self.fill_max_compensation(max_compensation)
        self.toggle_auto_approve_off()

    # ── Методы проверок ───────────────────────────────────────

    @allure.step("Проверка: страница создания кампании загружена")
    def expect_loaded(self) -> None:
        """Проверить что страница создания кампании загружена."""
        self.expect_url_contains(r".*/app/advertiser/campaigns/create")
        expect(self.heading).to_be_visible()

    @allure.step("Проверка: хлебные крошки видны")
    def check_breadcrumb_visible(self) -> None:
        """Проверить видимость хлебных крошек."""
        expect(self.breadcrumb_campaigns).to_be_visible()
        expect(self.breadcrumb_create).to_be_visible()

    @allure.step("Проверка: все поля формы видны")
    def check_form_fields_visible(self) -> None:
        """Проверить видимость всех полей формы."""
        expect(self.input_name).to_be_visible()
        expect(self.select_product).to_be_visible()
        expect(self.input_utm_link).to_be_visible()
        expect(self.content_format_label).to_be_visible()
        expect(self.thematic_label).to_be_visible()
        expect(self.input_task).to_be_visible()
        expect(self.heading_payment).to_be_visible()
        expect(self.tab_barter).to_be_visible()
        expect(self.input_max_compensation).to_be_visible()
        expect(self.switch_auto_approve).to_be_visible()
        expect(self.btn_create_campaign).to_be_visible()

    @allure.step("Проверка: таб Бартер выбран по умолчанию")
    def check_barter_tab_selected(self) -> None:
        """Проверить что таб Бартер выбран по умолчанию."""
        expect(self.tab_barter).to_have_attribute("aria-selected", "true")

    @allure.step("Проверка: Автоодобрение включено по умолчанию")
    def check_auto_approve_checked(self) -> None:
        """Проверить что switch Автоодобрение включен."""
        expect(self.switch_auto_approve).to_be_checked()

    @allure.step("Проверка: Автоодобрение выключено")
    def check_auto_approve_unchecked(self) -> None:
        """Проверить что switch Автоодобрение выключен."""
        expect(self.switch_auto_approve).not_to_be_checked()

    # ── Проверки ошибок валидации ──────────────────────────────

    @allure.step("Проверка: все ошибки валидации отображаются при пустой отправке")
    def check_all_validation_errors_visible(self) -> None:
        """Проверить что все 5 ошибок валидации отображаются."""
        count = self.all_errors.count()
        assert count >= 5, f"Ожидалось ≥5 ошибок валидации, получено {count}"

    @allure.step('Проверка: ошибка названия — "Обязательное поле"')
    def check_error_name(self) -> None:
        """Проверить ошибку поля Название."""
        expect(self.error_name).to_contain_text("Обязательное поле")

    @allure.step('Проверка: ошибка предмета рекламы — "Обязательное поле"')
    def check_error_product(self) -> None:
        """Проверить ошибку поля Предмет рекламы."""
        expect(self.error_product).to_contain_text("Обязательное поле")

    @allure.step('Проверка: ошибка формата контента — "Необходимо выбрать социальную сеть"')
    def check_error_content_format(self) -> None:
        """Проверить ошибку поля Формат контента."""
        expect(self.error_content_format).to_contain_text("Необходимо выбрать социальную сеть")

    @allure.step('Проверка: ошибка тематики — "Нужно выбрать хотя бы одну тематику."')
    def check_error_thematic(self) -> None:
        """Проверить ошибку поля Тематика."""
        expect(self.error_thematic).to_contain_text("Нужно выбрать хотя бы одну тематику")

    @allure.step('Проверка: ошибка задания — "Значение слишком маленькое. Минимум: 5"')
    def check_error_task(self) -> None:
        """Проверить ошибку поля Задание."""
        expect(self.error_task).to_contain_text("Значение слишком маленькое")

    @allure.step("Проверка: URL остаётся на странице создания (нет редиректа)")
    def check_still_on_create_page(self) -> None:
        """Проверить что после ошибки валидации остаёмся на странице создания."""
        self.expect_url_contains(r".*/app/advertiser/campaigns/create")

    @allure.step("Проверка: ошибки валидации отсутствуют")
    def check_no_errors(self) -> None:
        """Проверить что ошибок валидации нет."""
        count = self.all_errors.count()
        assert count == 0, f"Найдено {count} ошибок валидации, ожидалось 0"
