"""POM: Страница интеграции блогера — выполнение шагов интеграции."""
from pathlib import Path

import allure
from playwright.sync_api import Page, expect

from tests.pages.base_page import BasePage

WORKS_URL = "https://app.rizz.market/app/creator/works"
TEST_IMAGE_PATH = str(Path(__file__).resolve().parents[1] / "test_data" / "product_image.jpg")


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

        # ── Кнопки рекламодателя (принятие шагов) ────────────
        self.advertiser_chat_button = page.get_by_role("button", name="Чат с блогером")
        self.advertiser_message_input = page.locator(
            "textarea[placeholder='Наберите текст вашего сообщения']"
        )

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

        # ── Поле суммы (шаг "Подтверждение выкупа товара") ──────
        self.amount_input = self.page.locator("input[name='amount']")

    # ── Загрузка медиа (шаги интеграции) ──────────────────────

    @allure.step('Заполнить поле суммы значением "{amount}"')
    def fill_amount(self, amount: str) -> None:
        """Заполнить поле 'Введите сумму в рублях' в шаге подтверждения выкупа."""
        expect(self.amount_input).to_be_visible(timeout=10000)
        self.amount_input.fill(amount)

    def _get_submit_button(self):
        """Найти первую доступную кнопку "Отправить"."""
        return self.page.get_by_role("button", name="Отправить", exact=True).first

    def _click_submit_and_wait_processed(self) -> None:
        """Нажать первую доступную кнопку "Отправить" и дождаться обработки шага.

        Успех:
        - число кнопок "Отправить" уменьшилось, или
        - не осталось enabled-кнопок "Отправить".
        """
        submit_btn = self._get_submit_button()
        expect(submit_btn).to_be_visible(timeout=10000)
        expect(submit_btn).to_be_enabled(timeout=10000)

        submit_count_before = self.page.get_by_role(
            "button", name="Отправить", exact=True
        ).count()

        submit_btn.click()

        self.page.wait_for_function(
            """
            ({ beforeCount }) => {
              const submitButtons = Array.from(document.querySelectorAll('button'))
                .filter((btn) => (btn.textContent || '').includes('Отправить'));
              const enabledSubmitButtons = submitButtons.filter((btn) => !btn.disabled);
              return submitButtons.length < beforeCount || enabledSubmitButtons.length === 0;
            }
            """,
            arg={"beforeCount": submit_count_before},
            timeout=15000,
        )

    @allure.step('Загрузить медиа и отправить')
    def upload_media_and_submit(self, file_path: str = TEST_IMAGE_PATH) -> None:
        """Загрузить файл в первый доступный input[type=file] и отправить шаг."""
        file_input = self.file_inputs.first
        expect(file_input).to_be_attached(timeout=15000)
        file_input.set_input_files(file_path)

        # Небольшая пауза для рендера превью
        self.page.wait_for_timeout(1000)

        self._click_submit_and_wait_processed()

    @allure.step('Загрузить медиа, заполнить сумму и отправить (шаг подтверждения выкупа)')
    def upload_media_fill_amount_and_submit(
        self, amount: str = "100", file_path: str = TEST_IMAGE_PATH
    ) -> None:
        """Шаг 3: загрузить чек, заполнить сумму, отправить."""
        file_input = self.file_inputs.first
        expect(file_input).to_be_attached(timeout=15000)
        file_input.set_input_files(file_path)

        self.page.wait_for_timeout(1000)

        self.fill_amount(amount)

        self._click_submit_and_wait_processed()

    @allure.step('Выполнить загрузку медиа для первых 3 шагов')
    def upload_all_media_steps(self, count: int = 3, file_path: str = TEST_IMAGE_PATH) -> None:
        """Последовательно загрузить медиа и отправить для каждого из первых 3 шагов.

        Шаг 3 (подтверждение выкупа) дополнительно требует заполнения суммы.
        """
        for step in range(count):
            with allure.step(f"Загрузка медиа: шаг {step + 1} из {count}"):
                if step == 2:
                    self.upload_media_fill_amount_and_submit("100", file_path)
                else:
                    self.upload_media_and_submit(file_path)
                self.page.wait_for_timeout(3000)

    @allure.step('Загрузить медиа-контент (шаг 4)')
    def upload_media_content_step(self, file_path: str = TEST_IMAGE_PATH) -> None:
        """Шаг 4 — Медиа-контент: загрузить креатив для соц.сети и отправить."""
        file_input = self.file_inputs.first
        expect(file_input).to_be_attached(timeout=15000)
        file_input.set_input_files(file_path)

        self.page.wait_for_timeout(1000)

        self._click_submit_and_wait_processed()

    # ══════════════════════════════════════════════════════════
    # Методы рекламодателя — принятие шагов интеграции
    # ══════════════════════════════════════════════════════════

    @allure.step('Открыть страницу интеграций рекламодателя')
    def open_advertiser_works(self) -> None:
        self.page.goto(
            "https://app.rizz.market/app/advertiser/works",
            wait_until="networkidle",
        )

    @allure.step('Нажать на ник блогера "danil23319" в карточке')
    def click_blogger_nick_danil(self) -> None:
        nick = self.page.locator(
            "p.flex.items-center.gap-2.truncate.text-slate-500",
            has_text="danil23319",
        ).first
        expect(nick).to_be_visible(timeout=15_000)
        nick.click()
        self.page.wait_for_timeout(3_000)

    @allure.step("Принять все шаги интеграции с retry-логикой")
    def accept_all_steps(self, steps_count: int = 4, max_retries: int = 5) -> None:
        """Последовательно нажимает кнопку «Принять» steps_count раз.

        После каждого нажатия проверяет что кнопка исчезла.
        Если нет — повторяет (retry). Кнопки перенумеровываются
        после каждого принятия, поэтому всегда берём .first.
        """
        for step_index in range(steps_count):
            self._accept_single_step(step_index, max_retries)

    def _accept_single_step(self, step_index: int, max_retries: int) -> None:
        expected_remaining = 3 - step_index

        for attempt in range(1, max_retries + 1):
            accept_btn = self.page.get_by_role(
                "button", name="Принять", exact=True
            ).first

            try:
                expect(accept_btn).to_be_visible(timeout=10_000)
                expect(accept_btn).to_be_enabled(timeout=5_000)
            except Exception:
                return  # кнопка уже пропала — шаг принят

            with allure.step(
                f"Шаг {step_index + 1}: нажатие «Принять» (попытка {attempt})"
            ):
                accept_btn.click()
                self.page.wait_for_timeout(2_000)

            remaining = self.page.get_by_role(
                "button", name="Принять", exact=True
            ).count()

            if remaining <= expected_remaining:
                return

        raise AssertionError(
            f"Не удалось принять шаг {step_index + 1} за {max_retries} попыток"
        )

    @allure.step('Открыть чат с блогером (сторона рекламодателя)')
    def open_advertiser_chat(self) -> None:
        expect(self.advertiser_chat_button).to_be_visible(timeout=10_000)
        self.advertiser_chat_button.click()
        self.page.wait_for_timeout(3_000)

    @allure.step('Отправить сообщение от рекламодателя: "{text}"')
    def send_advertiser_message(self, text: str) -> None:
        expect(self.advertiser_message_input).to_be_visible(timeout=10_000)
        self.advertiser_message_input.click()
        self.advertiser_message_input.fill(text)
        self.advertiser_message_input.press("Enter")
