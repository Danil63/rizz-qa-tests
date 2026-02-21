"""Фикстура авторизации рекламодателя."""
import allure
import pytest
from playwright.sync_api import Page

from tests.flows.auth_flow import AuthFlow
from tests.pages.campaigns_page import CampaignsPage


ADVERTISER_PHONE = "79087814701"
ADVERTISER_PASSWORD = "89087814701"


@pytest.fixture()
@allure.title("Авторизация как рекламодатель")
def advertiser_page(page: Page) -> Page:
    """Авторизоваться как рекламодатель и вернуть page."""
    auth = AuthFlow(page)
    auth.login_with_phone(ADVERTISER_PHONE, ADVERTISER_PASSWORD)
    CampaignsPage(page).expect_loaded()

    cookie_btn = page.get_by_role("button", name="Принять cookie")
    if cookie_btn.is_visible(timeout=3000):
        cookie_btn.click()

    return page
