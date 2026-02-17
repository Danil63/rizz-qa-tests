"""PFA: Флоу авторизации — цепочки действий через несколько страниц."""
from playwright.sync_api import Page

from tests.pages.sign_in_page import SignInPage
from tests.pages.campaigns_page import CampaignsPage


class AuthFlow:
    """Page Flow Actions: сценарии авторизации."""

    def __init__(self, page: Page):
        self.page = page
        self.sign_in = SignInPage(page)
        self.campaigns = CampaignsPage(page)

    def login_with_phone(
        self, phone: str, password: str, timeout: int = 15000
    ) -> CampaignsPage:
        """Полный флоу: открыть форму → ввести данные → войти → campaigns."""
        self.sign_in.open_phone_form()
        self.sign_in.phone.fill(phone)
        self.sign_in.password.fill(password)
        self.sign_in.click_login()
        self.page.wait_for_url("**/app/advertiser/campaigns", timeout=timeout)
        return self.campaigns

    def login_expect_error(self, phone: str, password: str) -> SignInPage:
        """Флоу: попытка входа с ожиданием ошибки."""
        self.sign_in.open_phone_form()
        self.sign_in.phone.fill(phone)
        self.sign_in.password.fill(password)
        self.sign_in.click_login()
        return self.sign_in

    def login_empty_submit(self) -> SignInPage:
        """Флоу: нажать Войти без заполнения полей."""
        self.sign_in.open_phone_form()
        self.sign_in.click_login()
        return self.sign_in

    def login_phone_only(self, phone: str) -> SignInPage:
        """Флоу: ввести только телефон и нажать Войти."""
        self.sign_in.open_phone_form()
        self.sign_in.phone.fill(phone)
        self.sign_in.click_login()
        return self.sign_in

    def login_password_only(self, password: str) -> SignInPage:
        """Флоу: ввести только пароль и нажать Войти."""
        self.sign_in.open_phone_form()
        self.sign_in.password.fill(password)
        self.sign_in.click_login()
        return self.sign_in
