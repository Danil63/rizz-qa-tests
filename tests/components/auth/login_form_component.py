"""PCO: Компонент формы логина (телефон + пароль)."""
from playwright.sync_api import Page, expect

from tests.components.base_component import BaseComponent


class LoginFormComponent(BaseComponent):
    def __init__(self, page: Page):
        super().__init__(page)
        self.phone_input = page.get_by_placeholder("+7")
        self.password_input = page.get_by_label("Пароль")

    def fill(self, phone: str, password: str, delay: int = 50) -> None:
        self.phone_input.click()
        self.phone_input.type(phone, delay=delay)
        self.password_input.click()
        self.password_input.type(password, delay=delay)

    def clear_phone(self) -> None:
        self.phone_input.click()
        self.phone_input.fill("")

    def clear_password(self) -> None:
        self.password_input.click()
        self.password_input.fill("")

    def check_visible(self) -> None:
        expect(self.phone_input).to_be_visible()
        expect(self.password_input).to_be_visible()

    def check_empty_phone(self) -> None:
        expect(self.phone_input).to_have_value("")

    def check_empty_password(self) -> None:
        expect(self.password_input).to_have_value("")

    def check_password_masked(self) -> None:
        expect(self.password_input).to_have_attribute("type", "password")

    def get_phone_value(self) -> str:
        return self.phone_input.input_value()
