import pytest
from playwright.sync_api import Page

from tests.pages.sign_in_page import SignInPage
from tests.pages.campaigns_page import CampaignsPage
from tests.flows.auth_flow import AuthFlow


@pytest.fixture(scope="session")
def browser_context_args():
    return {
        "viewport": {"width": 1280, "height": 720},
        "locale": "ru-RU",
    }


@pytest.fixture()
def sign_in_page(page: Page) -> SignInPage:
    """POM: страница авторизации."""
    return SignInPage(page)


@pytest.fixture()
def campaigns_page(page: Page) -> CampaignsPage:
    """POM: страница кампаний."""
    return CampaignsPage(page)


@pytest.fixture()
def auth_flow(page: Page) -> AuthFlow:
    """PFA: флоу авторизации."""
    return AuthFlow(page)
