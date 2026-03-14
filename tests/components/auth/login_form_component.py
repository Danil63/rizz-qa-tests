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

    def fill_phone(self, phone: str, delay: int = 50) -> None:
        """Заполнить только поле телефона."""
        self.phone_input.click()
        self.phone_input.type(phone, delay=delay)

    def fill_password(self, password: str, delay: int = 50) -> None:
        """Заполнить только поле пароля."""
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

    def check_phone_mask(self) -> None:
        """Проверить что маска телефона содержит код страны."""
        value = self.phone_input.input_value()
        assert len(value) > 0, "Поле телефона пустое после ввода"
        assert "7" in value, "Маска не содержит код страны"

    def check_phone_auto_prefix(self) -> None:
        """Проверить автоподстановку +7."""
        value = self.phone_input.input_value()
        assert value.startswith("+7") or value.startswith("7"), (
            f"Автоподстановка +7 не сработала: '{value}'"
        )

    def get_phone_value(self) -> str:
        """Получить значение поля телефона."""
        return self.phone_input.input_value()

    def check_phone_has_error(self) -> None:
        """Проверить что поле телефона подсвечено ошибкой."""
        expect(self.phone_input).to_have_attribute("aria-invalid", "true")

    def check_password_has_error(self) -> None:
        """Проверить что поле пароля подсвечено ошибкой."""
        expect(self.password_input).to_have_attribute("aria-invalid", "true")

    def check_fields_have_errors(self) -> None:
        """Проверить что оба поля подсвечены ошибкой валидации."""
        self.check_phone_has_error()
        self.check_password_has_error()

    def check_phone_error_message(self, text: str) -> None:
        """Проверить текст ошибки валидации под полем телефона."""
        error_msg = self.page.locator(f'p:text-is("{text}")')
        expect(error_msg).to_be_visible(timeout=5000)

    def check_password_error_message(self, text: str) -> None:
        """Проверить текст ошибки валидации под полем пароля."""
        error_msg = self.page.locator(f'p:text-is("{text}")')
        expect(error_msg).to_be_visible(timeout=5000)
