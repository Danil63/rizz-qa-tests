"""PFA: Флоу авторизации."""
from playwright.sync_api import Page

from tests.pages.sign_in_page import SignInPage
from tests.pages.campaigns_page import CampaignsPage


class AuthFlow:
    def __init__(self, page: Page):
        self.page = page
        self.sign_in = SignInPage(page)
        self.campaigns = CampaignsPage(page)

    def login_with_phone(self, phone: str, password: str, timeout: int = 15000) -> CampaignsPage:
        self.sign_in.open_phone_form()
        self.sign_in.login_form.fill(phone, password)
        self.sign_in.click_login_button()
        self.page.wait_for_url("**/app/advertiser/campaigns", timeout=timeout)
        return self.campaigns

    def login_expect_error(self, phone: str, password: str) -> SignInPage:
        self.sign_in.open_phone_form()
        self.sign_in.login_form.fill(phone, password)
        self.sign_in.click_login_button()
        return self.sign_in

    def login_empty_submit(self) -> SignInPage:
        self.sign_in.open_phone_form()
        self.sign_in.click_login_button()
        return self.sign_in

    def login_phone_only(self, phone: str) -> SignInPage:
        self.sign_in.open_phone_form()
        self.sign_in.login_form.phone_input.click()
        self.sign_in.login_form.phone_input.type(phone, delay=50)
        self.sign_in.click_login_button()
        return self.sign_in

    def login_password_only(self, password: str) -> SignInPage:
        self.sign_in.open_phone_form()
        self.sign_in.login_form.password_input.click()
        self.sign_in.login_form.password_input.type(password, delay=50)
        self.sign_in.click_login_button()
        return self.sign_in
