"""POM: Повторная отправка отклика на бартер (cancel + reapply)."""
import allure
from playwright.sync_api import Page, expect

from tests.pages.base_page import BasePage


class CancelAndReapplyPage(BasePage):
    """Page Object для сценария отмены и повторной отправки отклика блогером."""

    URL = "https://app.rizz.market/app/creator/market"

    def __init__(self, page: Page):
        super().__init__(page)

        # Поиск
        self.search_input = page.get_by_role("textbox", name="Поиск")

        # Карточка / действия
        self.barter_button = page.get_by_role("button", name="Бартер").first
        self.cancel_response_button = page.get_by_role("button", name="Отменить отклик").first
        self.execute_barter_button = page.get_by_role("button", name="Выполнить за бартер").first

        # Соцсеть
        self.social_network_dropdown = page.locator("span", has_text="Социальная сеть").first
        self.social_network_danil_option = page.get_by_role("option", name="danil23319").first
        self.social_network_danil_button = page.get_by_role("button", name="danil23319").first
        self.social_network_danil_text = page.get_by_text("danil23319", exact=False).first

        # Отправка
        self.respond_barter_button = page.get_by_role("button", name="Откликнуться на бартер").first

        # Проверки
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
        expect(self.barter_button).to_be_visible(timeout=10000)
        expect(self.barter_button).to_be_enabled(timeout=10000)
        self.barter_button.click()

    @allure.step('Подождать 5 секунд и нажать кнопку "Отменить отклик"')
    def wait_and_click_cancel_response(self) -> None:
        self.page.wait_for_timeout(5000)
        expect(self.cancel_response_button).to_be_visible(timeout=10000)
        expect(self.cancel_response_button).to_be_enabled(timeout=10000)
        self.cancel_response_button.click()

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
        raise AssertionError('Не найден элемент выбора соцсети "danil23319" (option/button/text)')

    @allure.step('Подождать 5 секунд и нажать "Откликнуться на бартер"')
    def wait_and_click_respond_barter(self) -> None:
        self.page.wait_for_timeout(5000)
        expect(self.respond_barter_button).to_be_visible(timeout=10000)
        expect(self.respond_barter_button).to_be_enabled(timeout=10000)
        self.respond_barter_button.click()

    @allure.step('Подождать 5 секунд и проверить баннер обработки')
    def wait_and_check_processing_banner(self) -> None:
        self.page.wait_for_timeout(5000)
        expect(self.processing_banner).to_be_visible(timeout=10000)

    @allure.step('Подождать 5 секунд и проверить плашку "Отклик на бартер отправлен"')
    def wait_and_check_sent_badge(self) -> None:
        self.page.wait_for_timeout(5000)
        expect(self.sent_barter_badge).to_be_visible(timeout=10000)
