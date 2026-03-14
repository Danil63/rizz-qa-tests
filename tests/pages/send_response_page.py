"""POM: Отправка отклика на бартер/фиксированную выплату со страницы creator market."""

from playwright.sync_api import Page, expect

from tests.pages.base_page import BasePage


class SendResponsePage(BasePage):
    """Page Object для сценария отправки отклика блогером."""

    URL = "https://app.rizz.market/app/creator/market"

    def __init__(self, page: Page):
        super().__init__(page)

        # Поиск
        self.search_input = page.get_by_role("textbox", name="Поиск")

        # Элементы сценария
        self.barter_button = page.get_by_role("button", name="Бартер").first
        self.execute_barter_button = page.get_by_role(
            "button", name="Выполнить за бартер"
        ).first
        self.social_network_dropdown = page.locator(
            "span", has_text="Социальная сеть"
        ).first
        self.social_network_danil_button = page.get_by_role(
            "button", name="danil23319"
        ).first
        self.social_network_danil_option = page.get_by_role(
            "option", name="danil23319"
        ).first
        self.social_network_danil_text = page.get_by_text(
            "danil23319", exact=False
        ).first
        self.respond_barter_button = page.get_by_role(
            "button", name="Откликнуться на бартер"
        ).first

        # Финальные проверки
        self.processing_banner = page.get_by_text(
            "Отклик находится в обработке. Вы получите уведомление о результате."
        ).first
        self.sent_barter_badge = page.get_by_text("Отклик на бартер отправлен").first

    def open(self) -> None:
        self.page.goto(self.URL, wait_until="networkidle")

    def search_product_and_submit(self, product_name: str) -> None:
        self.search_input.click()
        self.search_input.fill(product_name)
        self.search_input.press("Enter")

    def wait_and_check_product_title(self, product_name: str) -> None:
        self.page.wait_for_timeout(2000)
        title = self.page.locator("h3", has_text=product_name).first
        expect(title).to_be_visible(timeout=10000)

    def wait_and_click_barter(self) -> None:
        self.page.wait_for_timeout(2000)
        self.barter_button.scroll_into_view_if_needed()
        expect(self.barter_button).to_be_visible(timeout=10000)
        expect(self.barter_button).to_be_enabled(timeout=10000)
        self.barter_button.click()

    def wait_and_click_execute_barter(self) -> None:
        self.page.wait_for_timeout(2000)
        expect(self.execute_barter_button).to_be_visible(timeout=10000)
        expect(self.execute_barter_button).to_be_enabled(timeout=10000)
        self.execute_barter_button.click()

    def wait_and_open_social_dropdown(self) -> None:
        self.page.wait_for_timeout(2000)
        expect(self.social_network_dropdown).to_be_visible(timeout=10000)
        self.social_network_dropdown.click()

    def wait_and_select_danil_account(self) -> None:
        self.page.wait_for_timeout(2000)

        candidates = [
            self.social_network_danil_option,
            self.social_network_danil_button,
            self.social_network_danil_text,
        ]

        for candidate in candidates:
            try:
                if candidate.count() > 0 and candidate.is_visible(timeout=2000):
                    candidate.click()
                    return
            except Exception:
                continue

        raise AssertionError(
            'Не найден элемент выбора соцсети "danil23319" (option/button/text)'
        )

    def wait_and_click_respond_barter(self) -> None:
        self.page.wait_for_timeout(2000)
        expect(self.respond_barter_button).to_be_visible(timeout=10000)
        expect(self.respond_barter_button).to_be_enabled(timeout=10000)
        self.respond_barter_button.click()

    def wait_and_check_processing_banner(self) -> None:
        self.page.wait_for_timeout(2000)
        expect(self.processing_banner).to_be_visible(timeout=10000)

    def wait_and_check_sent_badge(self) -> None:
        self.page.wait_for_timeout(2000)
        expect(self.sent_barter_badge).to_be_visible(timeout=10000)

    # ── Методы для фиксированной выплаты ─────────────────────────────

    def wait_and_click_fix_price_button(self, price: str) -> None:
        """Нажать кнопку с суммой вознаграждения на карточке кампании (вместо 'Бартер')."""
        self.page.wait_for_timeout(2000)
        btn = self.page.get_by_role("button", name=f"{price} ₽").first
        btn.scroll_into_view_if_needed()
        expect(btn).to_be_visible(timeout=10000)
        expect(btn).to_be_enabled(timeout=10000)
        btn.click()

    # ── Методы для CPM (За просмотры) ────────────────────────────────

    def wait_and_click_cpm_button(self) -> None:
        """Нажать кнопку CPM-кампании на карточке.

        CPM-кнопка отображается как "{rate} ₽за каждую 1К" (ставка за 1000 просмотров),
        в отличие от фиксированной оплаты где кнопка содержит только "{price} ₽".
        """
        import re
        self.page.wait_for_timeout(2000)
        btn = self.page.locator("button", has_text=re.compile(r"за каждую 1К")).first
        btn.scroll_into_view_if_needed()
        expect(btn).to_be_visible(timeout=10000)
        expect(btn).to_be_enabled(timeout=10000)
        btn.click()

    def click_execute_fix(self, price: str) -> None:
        """Нажать кнопку 'Выполнить за {price} ₽' внутри модалки и дождаться следующего шага."""
        btn = self.page.get_by_role("button", name="Выполнить за", exact=False)
        expect(btn).to_be_visible(timeout=10000)
        expect(btn).to_be_enabled(timeout=10000)
        btn.click()
        self.page.wait_for_timeout(2000)

    def open_social_dropdown_with_dom_check(self) -> None:
        """Открыть combobox 'Социальная сеть' и проверить что он открылся."""
        combobox = self.page.get_by_role("combobox")
        expect(combobox).to_be_visible(timeout=10000)

        # DOM до нажатия
        dom_before = combobox.evaluate("el => el.outerHTML")
        assert 'data-state="closed"' in dom_before, (
            "Ожидался закрытый combobox (data-state=closed) до клика"
        )

        combobox.click()
        self.page.wait_for_timeout(1500)

        # DOM после — листбокс должен появиться
        listbox = self.page.get_by_role("listbox")
        expect(listbox).to_be_visible(timeout=5000)

    def select_crazy_account(self) -> None:
        """Выбрать option 'ann.malevichh ' из listbox и проверить выбор через DOM."""
        option = self.page.get_by_role("option", name="ann.malevichh ")
        expect(option).to_be_visible(timeout=5000)
        option.click()
        self.page.wait_for_timeout(1500)

        # DOM после выбора: combobox должен показывать 'ann.malevichh '
        combobox = self.page.get_by_role("combobox")
        dom_after_select = combobox.evaluate("el => el.outerHTML")
        assert "ann.malevichh" in dom_after_select, (
            "Ожидалось, что combobox покажет 'ann.malevichh' после выбора"
        )

    def click_respond_cpm_and_check_modal_closed(self) -> None:
        """Нажать 'Начать сразу за ...' (CPM: цена рассчитывается динамически),
        подождать 3 секунды, нажать повторно и дождаться закрытия модалки."""
        import re
        btn = self.page.get_by_role("button", name=re.compile(r"Начать сразу за"))
        expect(btn).to_be_visible(timeout=10000)
        expect(btn).to_be_enabled(timeout=10000)

        # Первый клик
        btn.click()
        self.page.wait_for_timeout(3000)

        # Проверка: модальное окно закрылось
        dialogs = self.page.locator("[role=dialog]").all()
        for dialog in dialogs:
            assert not dialog.is_visible(), (
                "Модальное окно не закрылось спустя 3 секунды после нажатия 'Откликнуться'"
            )

    def click_respond_fix_and_check_modal_closed(self, price: str) -> None:
        """Нажать 'Откликнуться за {price} ₽' и убедиться, что модалка закрылась."""
        btn = self.page.get_by_role("button", name=f"Начать сразу за {price}")
        expect(btn).to_be_visible(timeout=10000)
        expect(btn).to_be_enabled(timeout=10000)

        btn.click()

        # Неявное ожидание 3 секунды
        self.page.wait_for_timeout(3000)

        # Проверка: модальное окно закрылось
        dialogs = self.page.locator("[role=dialog]").all()
        for dialog in dialogs:
            assert not dialog.is_visible(), (
                "Модальное окно не закрылось спустя 3 секунды после нажатия 'Откликнуться'"
            )
