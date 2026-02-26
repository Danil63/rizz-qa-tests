"""POM: Страница интеграции блогера — выполнение шагов интеграции."""
from pathlib import Path

import allure
from playwright.sync_api import Page, expect

from tests.pages.base_page import BasePage

WORKS_URL = "https://app.rizz.market/app/creator/works"
TEST_IMAGE_PATH = str(Path(__file__).resolve().parents[1] / "test_data" / "product_image.jpg")

# Заголовки секций шагов интеграции (порядок важен)
STEP_HEADINGS = [
    "Шаги выкупа товара (бартер)",
    "Отзыв",
    "Подтверждение выкупа товара",
    "Медиа-контент",
]


class IntegrationPage(BasePage):
    """Page Object для страницы выполнения интеграции блогером."""

    URL = f"{WORKS_URL}?filter=New"

    def __init__(self, page: Page):
        super().__init__(page)

        # ── Кнопка чата ───────────────────────────────────────
        self.chat_button = page.get_by_role("button", name="Чат с рекламодателем")

        # ── Чат: текстовое поле и сообщение ───────────────────
        self.chat_textarea = page.locator(
            "textarea[placeholder='Наберите текст вашего сообщения']"
        )

        # ── Кнопка "Начать работу" ────────────────────────────
        self.start_work_button = page.get_by_role("button", name="Начать работу")

        # ── Шаги загрузки медиа (4 input[type=file]) ─────────
        self.file_inputs = page.locator("input[type='file']")

    # ── Навигация ─────────────────────────────────────────────

    @allure.step('Открыть страницу интеграций (filter=New)')
    def open(self) -> None:
        self.page.goto(self.URL, wait_until="networkidle")

    @allure.step('Нажать на карточку продукта "{product_name}" (с retry)')
    def click_product_card(self, product_name: str, max_retries: int = 5) -> None:
        """Найти и кликнуть карточку по заголовку. Retry с перезагрузкой каждые 5 сек."""
        product_link = self.page.locator("span.line-clamp-2", has_text=product_name).first

        for attempt in range(max_retries):
            try:
                expect(product_link).to_be_visible(timeout=5000)
                product_link.click()
                return
            except Exception:
                if attempt < max_retries - 1:
                    self.page.wait_for_timeout(5000)
                    self.page.reload(wait_until="networkidle")

        raise AssertionError(
            f'Карточка "{product_name}" не найдена после {max_retries} попыток обновления'
        )

    # ── Чат ───────────────────────────────────────────────────

    @allure.step('Нажать "Чат с рекламодателем"')
    def click_chat_button(self) -> None:
        expect(self.chat_button).to_be_visible(timeout=10000)
        self.chat_button.click()

    @allure.step('Отправить сообщение в чат: "{text}"')
    def send_chat_message(self, text: str) -> None:
        expect(self.chat_textarea).to_be_visible(timeout=10000)
        self.chat_textarea.fill(text)
        self.chat_textarea.press("Enter")

    @allure.step('Проверить что сообщение "{text}" появилось в чате')
    def wait_for_chat_message(self, text: str) -> None:
        message = self.page.locator(
            "p.w-full.overflow-hidden.break-all.text-sm.font-normal",
            has_text=text,
        )
        expect(message).to_be_visible(timeout=10000)

    # ── Начать работу ─────────────────────────────────────────

    @allure.step('Нажать "Начать работу"')
    def click_start_work(self) -> None:
        expect(self.start_work_button).to_be_visible(timeout=10000)
        expect(self.start_work_button).to_be_enabled(timeout=10000)
        self.start_work_button.click()

    # ── Загрузка медиа (шаги интеграции) ──────────────────────

    def _get_step_section(self, heading_text: str):
        """Найти секцию шага по заголовку h3 — берём родительский контейнер."""
        heading = self.page.get_by_role("heading", name=heading_text)
        # Секция — ближайший общий предок, содержащий и h3, и кнопку Отправить
        return heading.locator("xpath=ancestor::div[.//button[@type='submit']]").first

    @allure.step('Загрузить медиа и отправить')
    def upload_media_and_submit(self, step_index: int, file_path: str = TEST_IMAGE_PATH) -> None:
        """Загрузить файл в input[type=file] по индексу и нажать Отправить в нужной секции."""
        file_input = self.file_inputs.nth(step_index)
        file_input.set_input_files(file_path)

        # Ожидание загрузки превью
        self.page.wait_for_timeout(2000)

        # Находим кнопку "Отправить" внутри секции по заголовку
        heading_text = STEP_HEADINGS[step_index]
        section = self._get_step_section(heading_text)
        submit_btn = section.locator("button[type='submit']", has_text="Отправить")

        expect(submit_btn).to_be_visible(timeout=10000)
        expect(submit_btn).to_be_enabled(timeout=10000)
        submit_btn.click()

        # Проверка: кнопка "Отправить" в этой секции пропала
        expect(submit_btn).not_to_be_visible(timeout=15000)

    @allure.step('Выполнить загрузку медиа для всех шагов')
    def upload_all_media_steps(self, count: int = 4, file_path: str = TEST_IMAGE_PATH) -> None:
        """Последовательно загрузить медиа и отправить для каждого шага."""
        for i in range(count):
            self.upload_media_and_submit(i, file_path)
            self.page.wait_for_timeout(2000)
