"""PCO: Компонент формы логина (телефон + пароль)."""
import allure
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

    @allure.step('Filling login form with phone and password')
    def fill(self, phone: str, password: str, delay: int = 50) -> None:
        """Заполнить форму авторизации (посимвольный ввод)."""
        self.phone_input.click()
        self.phone_input.type(phone, delay=delay)
        self.password_input.click()
        self.password_input.type(password, delay=delay)

    @allure.step('Clearing phone input')
    def clear_phone(self) -> None:
        """Очистить поле телефона."""
        self.phone_input.click()
        self.phone_input.fill("")

    @allure.step('Clearing password input')
    def clear_password(self) -> None:
        """Очистить поле пароля."""
        self.password_input.click()
        self.password_input.fill("")

    # ── Методы проверок ───────────────────────────────────────

    @allure.step('Checking login form is visible')
    def check_visible(self) -> None:
        """Проверить что форма отображается."""
        expect(self.phone_input).to_be_visible()
        expect(self.password_input).to_be_visible()

    @allure.step('Checking phone input is empty')
    def check_empty_phone(self) -> None:
        """Проверить что поле телефона пустое."""
        expect(self.phone_input).to_have_value("")

    @allure.step('Checking password input is empty')
    def check_empty_password(self) -> None:
        """Проверить что поле пароля пустое."""
        expect(self.password_input).to_have_value("")

    @allure.step('Checking password is masked (type=password)')
    def check_password_masked(self) -> None:
        """Проверить что пароль скрыт (type=password)."""
        expect(self.password_input).to_have_attribute("type", "password")

    def get_phone_value(self) -> str:
        """Получить значение поля телефона."""
        return self.phone_input.input_value()
