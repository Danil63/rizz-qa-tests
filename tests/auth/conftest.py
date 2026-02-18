import pytest
from playwright.sync_api import Page

from tests.pages.landing_page import LandingPage
from tests.pages.sign_in_page import SignInPage
from tests.pages.campaigns_page import CampaignsPage


@pytest.fixture(scope="session")
def browser_context_args():
    return {
        "viewport": {"width": 2560, "height": 1600},
        "locale": "ru-RU",
    }


@pytest.fixture(scope="session")
def browser_type_launch_args():
    return {
        "args": ["--start-maximized"],
        "headless": False,
    }


@pytest.fixture()
def landing_page(page: Page) -> LandingPage:
    """POM: лендинг rizz.market."""
    return LandingPage(page)


@pytest.fixture()
def sign_in_page(page: Page) -> SignInPage:
    """POM: страница авторизации."""
    return SignInPage(page)


@pytest.fixture()
def campaigns_page(page: Page) -> CampaignsPage:
    """POM: страница кампаний."""
    return CampaignsPage(page)
