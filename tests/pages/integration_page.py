"""POM: Страница интеграции блогера — выполнение шагов интеграции."""

from pathlib import Path

from playwright.sync_api import Page, expect

from tests.pages.base_page import BasePage

WORKS_URL = "https://app.rizz.market/app/creator/works"
TEST_IMAGE_PATH = str(
    Path(__file__).resolve().parents[1] / "test_data" / "product_image.jpg"
)
TEST_VIDEO_PATH = str(
    Path(__file__).resolve().parents[1] / "test_data" / "sample-5s.mp4"
)

# ── Локаторы блока «Размещение в социальной сети» (step-4) ────────────
# На странице рекламодателя существует ДВА элемента с id="step-4",
# поэтому используем уточнённый CSS-селектор по классу карточки.
STEP4_CARD = "div.rounded-lg.border.bg-card[id='step-4']"

# ── Локаторы блока «Выплата бартерного вознаграждения» (step-5) ────────
STEP5_CARD = "div.rounded-lg.border.bg-card[id='step-5']"
# Кнопка запуска выплаты — видна ДО запуска (исчезает после)
STEP5_START_PAYOUT_BTN = f"{STEP5_CARD} button:has-text('Запустить выплату')"
# Ссылка на акт — появляется ТОЛЬКО после успешного запуска выплаты (ответ сервера)
STEP5_ACT_LINK = f"{STEP5_CARD} a[download]"
# Кнопка «Подписать» — появляется после появления акта
STEP5_SIGN_BTN = f"{STEP5_CARD} form button[type='button']:has-text('Подписать')"

# Кнопки действий рекламодателя
BUTTON_ACCEPT_LINK = f"{STEP4_CARD} button[type='button']:has-text('Принять')"
BUTTON_REJECT_LINK = f"{STEP4_CARD} button[type='button'][aria-haspopup='dialog']"

# Статус-бейдж в заголовке карточки (rounded-full).
# ДО принятия: текст начинается с «Проверка до ...»
# ПОСЛЕ принятия: текст начинается с «Принят ...»
STEP4_STATUS_BADGE = f"{STEP4_CARD} div.rounded-full"


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

    def open(self) -> None:
        self.page.goto(self.URL, wait_until="networkidle")

    def click_product_card(self, product_name: str, max_retries: int = 5) -> None:
        """Найти и кликнуть карточку по заголовку. Retry с перезагрузкой каждые 5 сек."""
        product_link = self.page.locator(
            "span.line-clamp-2", has_text=product_name
        ).first

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

    def click_chat_button(self) -> None:
        expect(self.chat_button).to_be_visible(timeout=10000)
        self.chat_button.click()

    def send_chat_message(self, text: str) -> None:
        expect(self.chat_textarea).to_be_visible(timeout=10000)
        self.chat_textarea.fill(text)
        self.chat_textarea.press("Enter")

    def wait_for_chat_message(self, text: str) -> None:
        message = self.page.locator(
            "p.w-full.overflow-hidden.break-all.text-sm.font-normal",
            has_text=text,
        )
        expect(message).to_be_visible(timeout=10000)

    # ── Начать работу ─────────────────────────────────────────

    def click_start_work(self) -> None:
        expect(self.start_work_button).to_be_visible(timeout=10000)
        expect(self.start_work_button).to_be_enabled(timeout=10000)
        self.start_work_button.click()

        # ── Поле суммы (шаг "Подтверждение выкупа товара") ──────
        self.amount_input = self.page.locator("input[name='amount']")

    # ── Загрузка медиа (шаги интеграции) ──────────────────────

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

    def upload_media_and_submit(self, file_path: str = TEST_IMAGE_PATH) -> None:
        """Загрузить файл в первый доступный input[type=file] и отправить шаг."""
        file_input = self.file_inputs.first
        expect(file_input).to_be_attached(timeout=15000)
        file_input.set_input_files(file_path)

        # Небольшая пауза для рендера превью
        self.page.wait_for_timeout(1000)

        self._click_submit_and_wait_processed()

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

    def upload_all_media_steps(
        self, count: int = 3, file_path: str = TEST_IMAGE_PATH
    ) -> None:
        """Последовательно загрузить медиа и отправить для шагов 1–3 (максимум 3).

        Шаг 3 (подтверждение выкупа) дополнительно требует заполнения суммы.
        Шаг 4 (Медиа-контент, видео) выполняется отдельно через upload_step4_media_and_submit.
        """
        steps = min(count, 3)
        for step in range(steps):
            if step == 2:
                self.upload_media_fill_amount_and_submit("100", file_path)
            else:
                self.upload_media_and_submit(file_path)
            self.page.wait_for_timeout(3000)

    def upload_step4_media_and_submit(
        self,
        video_path: str = TEST_VIDEO_PATH,
        max_retries: int = 3,
        step_id: str = "step-3",
    ) -> None:
        """Загрузить видео в блок «Медиа-контент» и отправить.

        step_id: DOM-id блока с видео.
          - barter-кампания: "step-3" (по умолчанию)
          - fix-кампания:    "step-2"

        После set_input_files ждёт:
        1. Появления <video> — файл принят DOM-ом.
        2. Исчезновения progressbar — обработка превью завершена.
        Затем кликает «Отправить» с retry-логикой.
        """
        video_input = self.page.locator(
            '//h3[text()="Медиа-контент"]/following::input[@accept="video/*"][1]'
        )
        expect(video_input).to_be_attached(timeout=15_000)

        for attempt in range(1, max_retries + 1):
            video_input.set_input_files(video_path)

            # Ждём появления тега <video> — файл принят
            expect(self.page.locator(f"#{step_id} video")).to_be_visible(timeout=10_000)

            # Ждём исчезновения progressbar — превью готово
            expect(self.page.locator(f'#{step_id} [role="progressbar"]')).to_be_hidden(
                timeout=15_000
            )

            submit_count_before = self.page.get_by_role(
                "button", name="Отправить", exact=True
            ).count()

            self._click_submit_and_wait_processed()

            remaining = self.page.get_by_role(
                "button", name="Отправить", exact=True
            ).count()

            if remaining < submit_count_before:
                return

            if attempt < max_retries:
                self.page.wait_for_timeout(2_000)

        raise AssertionError(
            f"Шаг 4: не удалось отправить видео за {max_retries} попытки"
        )

    # ══════════════════════════════════════════════════════════
    # Методы рекламодателя — принятие шагов интеграции
    # ══════════════════════════════════════════════════════════

    def open_advertiser_works(self) -> None:
        self.page.goto(
            "https://app.rizz.market/app/advertiser/works",
            wait_until="networkidle",
        )

    def click_blogger_nick_danil(self) -> None:
        nick = self.page.locator(
            "p.flex.items-center.gap-2.truncate.text-slate-500",
            has_text="danil23319",
        ).first
        expect(nick).to_be_visible(timeout=15_000)
        nick.click()
        self.page.wait_for_timeout(3_000)

    def accept_all_steps(self, max_retries: int = 5) -> None:
        """Последовательно нажимает кнопку «Принять» 4 раза.

        После каждого нажатия проверяет что кнопка исчезла.
        Если нет — повторяет (retry). Кнопки перенумеровываются
        после каждого принятия, поэтому всегда берём .first.
        """
        for step_index in range(4):
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

    # ── Размещение в социальной сети (step-4) ─────────────────

    def fill_publication_link(self, url: str) -> None:
        """Заполнить поле «Ссылка на публикацию» в блоке step-4."""
        input_field = self.page.locator("#step-4 input[name='value']")
        expect(input_field).to_be_visible(timeout=10_000)
        input_field.fill(url)

    def submit_publication_link_with_retry(
        self,
        url: str,
        max_retries: int = 3,
        wait_timeout_ms: int = 5_000,
    ) -> None:
        """Скроллит к блоку «Размещение в социальной сети», вводит ссылку и нажимает «Отправить».

        Retry-логика: после каждого нажатия ждёт появления <a href="{url}"> в #step-4.
        Этот элемент рендерится только после успешного ответа сервера (GraphQL),
        поэтому его наличие гарантирует что ссылка реально сохранена — в отличие от
        простого исчезновения кнопки, которое может произойти во время анимации.
        Если ссылка не появилась — повторяет нажатие. После max_retries — AssertionError.
        """
        section = self.page.locator("#step-4")
        expect(section).to_be_visible(timeout=10_000)
        section.scroll_into_view_if_needed()

        submit_btn = self.page.locator(
            "#step-4 button:has-text('Отправить')"
        )
        # Появляется ТОЛЬКО после успешного сохранения на сервере
        saved_link = self.page.locator(f"#step-4 a[href='{url}']")

        for attempt in range(1, max_retries + 1):
            self.fill_publication_link(url)
            expect(submit_btn).to_be_visible(timeout=10_000)
            expect(submit_btn).to_be_enabled(timeout=5_000)
            submit_btn.click()
            try:
                # Ссылка <a href="{url}"> появляется только после ответа сервера
                expect(saved_link).to_be_visible(timeout=wait_timeout_ms)
                return  # сервер подтвердил — ссылка сохранена
            except Exception:
                if attempt == max_retries:
                    raise AssertionError(
                        f"Ссылка не сохранена на сервере после {max_retries} попыток. "
                        f"URL: {url}"
                    )

    # ── Принятие/отклонение ссылки на публикацию (step-4, рекламодатель) ──

    def scroll_to_social_link_step(self) -> None:
        """Скроллит к карточке step-4 на странице рекламодателя."""
        card = self.page.locator(STEP4_CARD)
        expect(card).to_be_visible(timeout=10_000)
        card.scroll_into_view_if_needed()

    def accept_publication_link_with_retry(
        self, max_retries: int = 3, wait_timeout_ms: int = 5_000
    ) -> None:
        """Нажимает «Принять» для шага «Размещение в социальной сети».

        Гарантированная проверка успеха: статус-бейдж карточки меняется
        с «Проверка до …» → «Принят …» только после ответа GraphQL-мутации
        ReviewWorkStepV2. Это надёжнее, чем проверять исчезновение кнопки
        (кнопка может пропасть в анимации до ответа сервера).
        """
        self.scroll_to_social_link_step()

        accept_btn = self.page.locator(BUTTON_ACCEPT_LINK)
        # Статус-бейдж — меняется ТОЛЬКО после успешного ответа сервера
        status_badge = self.page.locator(STEP4_STATUS_BADGE)

        for attempt in range(1, max_retries + 1):
            expect(accept_btn).to_be_visible(timeout=10_000)
            expect(accept_btn).to_be_enabled(timeout=5_000)
            accept_btn.click()
            try:
                # Бейдж «Принят …» появляется только после ReviewWorkStepV2 от сервера
                expect(status_badge).to_contain_text(
                    "Принят", timeout=wait_timeout_ms
                )
                return  # сервер подтвердил принятие
            except Exception:
                if attempt == max_retries:
                    raise AssertionError(
                        f"Статус шага не изменился на «Принят» после {max_retries} попыток. "
                        f"Ожидался бейдж с текстом «Принят» в {STEP4_CARD}."
                    )

    def check_publication_link_accepted(self) -> None:
        """Финальная проверка после принятия:
        1. Статус-бейдж содержит «Принят» (ответ сервера).
        2. Кнопки «Принять» и «Отклонить» отсутствуют (UI обновлён).
        """
        status_badge = self.page.locator(STEP4_STATUS_BADGE)
        expect(status_badge).to_contain_text("Принят", timeout=10_000)

        accept_btn = self.page.locator(BUTTON_ACCEPT_LINK)
        reject_btn = self.page.locator(BUTTON_REJECT_LINK)
        expect(accept_btn).not_to_be_visible(timeout=5_000)
        expect(reject_btn).not_to_be_visible(timeout=5_000)

    def click_reject_publication_link(self) -> None:
        """Открывает диалог отклонения (кнопка с aria-haspopup=dialog)."""
        self.scroll_to_social_link_step()
        reject_btn = self.page.locator(BUTTON_REJECT_LINK)
        expect(reject_btn).to_be_visible(timeout=10_000)
        expect(reject_btn).to_be_enabled(timeout=5_000)
        reject_btn.click()

    def open_advertiser_chat(self) -> None:
        expect(self.advertiser_chat_button).to_be_visible(timeout=10_000)
        self.advertiser_chat_button.click()
        self.page.wait_for_timeout(3_000)

    def send_advertiser_message(self, text: str) -> None:
        expect(self.advertiser_message_input).to_be_visible(timeout=10_000)
        self.advertiser_message_input.click()
        self.advertiser_message_input.fill(text)
        self.advertiser_message_input.press("Enter")

    # ══════════════════════════════════════════════════════════
    # Методы блогера — Выплата бартерного вознаграждения (step-5)
    # ══════════════════════════════════════════════════════════

    def expect_integration_page(self) -> None:
        """Проверяет два признака страницы интеграции:
        1. h2.title с текстом «Интеграция» — заголовок раздела.
        2. Breadcrumb [aria-current="page"] видим — финальный элемент хлебных крошек.
        Совместная проверка надёжнее одного локатора.
        """
        expect(self.page.locator("h2.title")).to_have_text("Интеграция", timeout=15000)
        expect(
            self.page.locator('nav[aria-label="breadcrumb"] [aria-current="page"]')
        ).to_be_visible(timeout=15000)

    def scroll_to_payout_step(self) -> None:
        """Прокручивает страницу к карточке step-5."""
        card = self.page.locator(STEP5_CARD)
        expect(card).to_be_visible(timeout=15000)
        card.scroll_into_view_if_needed()

    def click_start_payout(self) -> None:
        """Нажимает «Запустить выплату» и ждёт появления ссылки на акт.

        DOM до нажатия: кнопка «Запустить выплату» видима, ссылки a[download] нет.
        DOM после нажатия: появляется <a download> — «Акт выполненных работ».
        Это гарантирует что сервер обработал запрос, а не просто скрыл кнопку.
        """
        start_btn = self.page.locator(STEP5_START_PAYOUT_BTN)
        act_link = self.page.locator(STEP5_ACT_LINK)

        expect(start_btn).to_be_visible(timeout=15_000)
        expect(start_btn).to_be_enabled(timeout=10_000)
        # Проверяем DOM до: акта ещё нет
        expect(act_link).not_to_be_visible(timeout=8_000)

        start_btn.click()

        # Проверяем DOM после: акт появился (ответ сервера получен)
        expect(act_link).to_be_visible(timeout=15000)

    def wait_for_sign_button(self) -> None:
        """Явное ожидание кнопки «Подписать» после запуска выплаты."""
        sign_btn = self.page.locator(STEP5_SIGN_BTN)
        expect(sign_btn).to_be_visible(timeout=15000)
        expect(sign_btn).to_be_enabled(timeout=10000)
