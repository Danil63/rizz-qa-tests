"""POM: Отправка отклика на бартер/фиксированную выплату со страницы creator market."""

import allure
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

    @allure.step("Открыть страницу creator market")
    def open(self) -> None:
        self.page.goto(self.URL, wait_until="networkidle")

    @allure.step('Ввести запрос "{product_name}" и нажать Enter')
    def search_product_and_submit(self, product_name: str) -> None:
        self.search_input.click()
        self.search_input.fill(product_name)
        self.search_input.press("Enter")

    @allure.step('Подождать 5 секунд и проверить заголовок карточки "{product_name}"')
    def wait_and_check_product_title(self, product_name: str) -> None:
        self.page.wait_for_timeout(5000)
        title = self.page.locator("h3", has_text=product_name).first
        expect(title).to_be_visible(timeout=10000)

    @allure.step('Подождать 5 секунд и нажать кнопку "Бартер"')
    def wait_and_click_barter(self) -> None:
        self.page.wait_for_timeout(5000)
        self.barter_button.scroll_into_view_if_needed()
        expect(self.barter_button).to_be_visible(timeout=10000)
        expect(self.barter_button).to_be_enabled(timeout=10000)
        self.barter_button.click()

    @allure.step('Подождать 5 секунд и нажать кнопку "Выполнить за бартер"')
    def wait_and_click_execute_barter(self) -> None:
        self.page.wait_for_timeout(5000)
        expect(self.execute_barter_button).to_be_visible(timeout=10000)
        expect(self.execute_barter_button).to_be_enabled(timeout=10000)
        self.execute_barter_button.click()

    @allure.step('Подождать 5 секунд и открыть dropdown "Социальная сеть"')
    def wait_and_open_social_dropdown(self) -> None:
        self.page.wait_for_timeout(5000)
        expect(self.social_network_dropdown).to_be_visible(timeout=10000)
        self.social_network_dropdown.click()

    @allure.step('Подождать 5 секунд и выбрать "danil23319"')
    def wait_and_select_danil_account(self) -> None:
        self.page.wait_for_timeout(5000)

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

    @allure.step('Подождать 5 секунд и нажать "Откликнуться на бартер"')
    def wait_and_click_respond_barter(self) -> None:
        self.page.wait_for_timeout(5000)
        expect(self.respond_barter_button).to_be_visible(timeout=10000)
        expect(self.respond_barter_button).to_be_enabled(timeout=10000)
        self.respond_barter_button.click()

    @allure.step("Подождать 5 секунд и проверить баннер обработки")
    def wait_and_check_processing_banner(self) -> None:
        self.page.wait_for_timeout(5000)
        expect(self.processing_banner).to_be_visible(timeout=10000)

    @allure.step('Подождать 5 секунд и проверить плашку "Отклик на бартер отправлен"')
    def wait_and_check_sent_badge(self) -> None:
        self.page.wait_for_timeout(5000)
        expect(self.sent_barter_badge).to_be_visible(timeout=10000)

    # ── Методы для фиксированной выплаты ─────────────────────────────

    @allure.step('Подождать 5 секунд и нажать кнопку с суммой "{price} ₽" на карточке')
    def wait_and_click_fix_price_button(self, price: str) -> None:
        """Нажать кнопку с суммой вознаграждения на карточке кампании (вместо 'Бартер')."""
        self.page.wait_for_timeout(5000)
        btn = self.page.get_by_role("button", name=f"{price} ₽").first
        btn.scroll_into_view_if_needed()
        expect(btn).to_be_visible(timeout=10000)
        expect(btn).to_be_enabled(timeout=10000)
        btn.click()

    @allure.step('Нажать кнопку "Выполнить за {price} ₽"')
    def click_execute_fix(self, price: str) -> None:
        """Нажать кнопку 'Выполнить за {price} ₽' и дождаться открытия модалки."""
        btn = self.page.get_by_role("button", name=f"Выполнить за {price}")
        expect(btn).to_be_visible(timeout=10000)
        expect(btn).to_be_enabled(timeout=10000)
        btn.click()
        self.page.wait_for_timeout(2000)

    @allure.step('Открыть dropdown "Социальная сеть" (зафиксировать DOM до и после)')
    def open_social_dropdown_with_dom_check(self) -> None:
        """Открыть combobox 'Социальная сеть', прикрепить DOM до и после к Allure."""
        combobox = self.page.get_by_role("combobox")
        expect(combobox).to_be_visible(timeout=10000)

        # DOM до нажатия
        dom_before = combobox.evaluate("el => el.outerHTML")
        allure.attach(
            dom_before,
            name="DOM combobox BEFORE click (data-state=closed)",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert 'data-state="closed"' in dom_before, (
            "Ожидался закрытый combobox (data-state=closed) до клика"
        )

        combobox.click()
        self.page.wait_for_timeout(1500)

        # DOM после — листбокс должен появиться
        listbox = self.page.get_by_role("listbox")
        expect(listbox).to_be_visible(timeout=5000)
        dom_after = listbox.evaluate("el => el.outerHTML")
        allure.attach(
            dom_after,
            name="DOM listbox AFTER click (options visible)",
            attachment_type=allure.attachment_type.TEXT,
        )

    @allure.step('Выбрать соцсеть "crazy.6.3" и зафиксировать DOM после выбора')
    def select_crazy_account(self) -> None:
        """Выбрать option 'crazy.6.3' из listbox и проверить выбор через DOM."""
        option = self.page.get_by_role("option", name="crazy.6.3")
        expect(option).to_be_visible(timeout=5000)
        option.click()
        self.page.wait_for_timeout(1500)

        # DOM после выбора: combobox должен показывать 'crazy.6.3'
        combobox = self.page.get_by_role("combobox")
        dom_after_select = combobox.evaluate("el => el.outerHTML")
        allure.attach(
            dom_after_select,
            name="DOM combobox AFTER selecting crazy.6.3",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert "crazy.6.3" in dom_after_select, (
            "Ожидалось, что combobox покажет 'crazy.6.3' после выбора"
        )

    @allure.step('Нажать "Начать сразу за ..." и проверить закрытие модалки через 3 сек')
    def click_respond_cpm_and_check_modal_closed(self) -> None:
        """Нажать 'Начать сразу за ...' (CPM: цена в кнопке рассчитывается динамически)
        и убедиться, что модалка закрылась."""
        import re
        btn = self.page.get_by_role("button", name=re.compile(r"Начать сразу за"))
        expect(btn).to_be_visible(timeout=10000)
        expect(btn).to_be_enabled(timeout=10000)

        # DOM кнопки до клика
        dom_btn = btn.evaluate("el => el.outerHTML")
        allure.attach(
            dom_btn,
            name="DOM кнопки 'Начать сразу за' BEFORE click",
            attachment_type=allure.attachment_type.TEXT,
        )

        btn.click()

        # Неявное ожидание 3 секунды
        self.page.wait_for_timeout(3000)

        # Проверка: модальное окно закрылось
        dialogs = self.page.locator("[role=dialog]").all()
        for dialog in dialogs:
            assert not dialog.is_visible(), (
                "Модальное окно не закрылось спустя 3 секунды после нажатия 'Начать сразу за'"
            )
        allure.attach(
            f"Dialogs visible after 3s: {len([d for d in dialogs if d.is_visible()])}",
            name="Состояние диалогов через 3 сек",
            attachment_type=allure.attachment_type.TEXT,
        )

    @allure.step('Нажать "Откликнуться за {price} ₽" и проверить закрытие модалки через 3 сек')
    def click_respond_fix_and_check_modal_closed(self, price: str) -> None:
        """Нажать 'Откликнуться за {price} ₽' и убедиться, что модалка закрылась."""
        btn = self.page.get_by_role("button", name=f"Откликнуться за {price}")
        expect(btn).to_be_visible(timeout=10000)
        expect(btn).to_be_enabled(timeout=10000)

        # DOM кнопки до клика
        dom_btn = btn.evaluate("el => el.outerHTML")
        allure.attach(
            dom_btn,
            name="DOM кнопки 'Откликнуться за' BEFORE click",
            attachment_type=allure.attachment_type.TEXT,
        )

        btn.click()

        # Неявное ожидание 3 секунды
        self.page.wait_for_timeout(3000)

        # Проверка: модальное окно закрылось
        dialogs = self.page.locator("[role=dialog]").all()
        for dialog in dialogs:
            assert not dialog.is_visible(), (
                "Модальное окно не закрылось спустя 3 секунды после нажатия 'Откликнуться'"
            )
        allure.attach(
            f"Dialogs visible after 3s: {len([d for d in dialogs if d.is_visible()])}",
            name="Состояние диалогов через 3 сек",
            attachment_type=allure.attachment_type.TEXT,
        )
