"""PCO: Компонент формы логина (телефон + пароль)."""
from playwright.sync_api import Page, expect

from tests.components.base_component import BaseComponent


class LoginFormComponent(BaseComponent):
    """Компонент формы авторизации по телефону и паролю."""

    def __init__(self, page: Page):
        super().__init__(page)

        # Локаторы элементов формы
        self.phone_input = page.get_by_placeholder("+7")
        self.password_input = page.get_by_label("Пароль")

    # ── Методы действий ───────────────────────────────────────

    def fill(self, phone: str, password: str, delay: int = 50) -> None:
        """Заполнить форму авторизации (посимвольный ввод)."""
        self.phone_input.click()
        self.phone_input.type(phone, delay=delay)
        self.password_input.click()
        self.password_input.type(password, delay=delay)

    def clear_phone(self) -> None:
        """Очистить поле телефона."""
        self.phone_input.click()
        self.phone_input.fill("")

    def clear_password(self) -> None:
        """Очистить поле пароля."""
        self.password_input.click()
        self.password_input.fill("")

    # ── Методы проверок ───────────────────────────────────────

    def check_visible(self) -> None:
        """Проверить что форма отображается."""
        expect(self.phone_input).to_be_visible()
        expect(self.password_input).to_be_visible()

    def check_empty_phone(self) -> None:
        """Проверить что поле телефона пустое."""
        expect(self.phone_input).to_have_value("")

    def check_empty_password(self) -> None:
        """Проверить что поле пароля пустое."""
        expect(self.password_input).to_have_value("")

    def check_password_masked(self) -> None:
        """Проверить что пароль скрыт (type=password)."""
        expect(self.password_input).to_have_attribute("type", "password")

    def get_phone_value(self) -> str:
        """Получить значение поля телефона."""
        return self.phone_input.input_value()
