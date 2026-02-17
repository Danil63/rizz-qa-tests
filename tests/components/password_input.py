"""PCO: Компонент ввода пароля (переиспользуемый)."""
from playwright.sync_api import Page, Locator, expect


class PasswordInput:
    """Универсальный компонент поля пароля."""

    def __init__(self, page: Page, label: str = "Пароль"):
        self._page = page
        self._label = label

    @property
    def locator(self) -> Locator:
        return self._page.get_by_label(self._label)

    def fill(self, password: str, delay: int = 50) -> None:
        """Посимвольный ввод пароля."""
        self.locator.click()
        self.locator.type(password, delay=delay)

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

    def expect_masked(self):
        """Проверить что пароль скрыт (type=password)."""
        expect(self.locator).to_have_attribute("type", "password")
