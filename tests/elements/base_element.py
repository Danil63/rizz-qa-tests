"""PageFactory: Базовый элемент — общий интерфейс для всех элементов."""
from playwright.sync_api import Page, Locator, expect


class BaseElement:
    """Базовый класс элемента. Не используется напрямую в тестах."""

    def __init__(self, page: Page, locator: str, name: str):
        self.page = page
        self.name = name
        self.locator = locator

    def get_locator(self, nth: int = 0, **kwargs) -> Locator:
        locator = self.locator.format(**kwargs)
        return self.page.locator(locator).nth(nth)

    def click(self, nth: int = 0, **kwargs) -> None:
        locator = self.get_locator(nth, **kwargs)
        locator.click()

    def check_visible(self, nth: int = 0, **kwargs) -> None:
        locator = self.get_locator(nth, **kwargs)
        expect(locator).to_be_visible()

    def check_have_text(self, text: str, nth: int = 0, **kwargs) -> None:
        locator = self.get_locator(nth, **kwargs)
        expect(locator).to_have_text(text)
