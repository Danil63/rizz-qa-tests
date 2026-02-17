"""PCO: Компонент ввода телефона (переиспользуемый)."""
from playwright.sync_api import Page, Locator, expect


class PhoneInput:
    """Универсальный компонент поля телефона с маской."""

    def __init__(self, page: Page, placeholder: str = "+7"):
        self._page = page
        self._placeholder = placeholder

    @property
    def locator(self) -> Locator:
        return self._page.get_by_placeholder(self._placeholder)

    def fill(self, phone: str, delay: int = 50) -> None:
        """Посимвольный ввод телефона."""
        self.locator.click()
        self.locator.type(phone, delay=delay)

    def clear(self) -> None:
        self.locator.click()
        self.locator.fill("")

    def get_value(self) -> str:
        return self.locator.input_value()

    def is_visible(self) -> bool:
        return self.locator.is_visible()

    def expect_visible(self):
        expect(self.locator).to_be_visible()

    def expect_empty(self):
        expect(self.locator).to_have_value("")

    def expect_has_value(self):
        value = self.get_value()
        assert len(value) > 0, "Поле телефона пустое"
