import pytest
from playwright.sync_api import Page


@pytest.fixture(scope="session")
def browser_context_args():
    return {
        "viewport": {"width": 1280, "height": 720},
        "locale": "ru-RU",
    }


@pytest.fixture()
def authenticated_page(page: Page) -> Page:
    """Авторизация через телефон+пароль, возвращает page на странице кампаний."""
    page.goto("https://app.rizz.market/auth/sign-in")
    page.get_by_role("button", name="Другие способы входа").click()
    page.get_by_placeholder("+7").click()
    page.get_by_placeholder("+7").type("+79087814701", delay=50)
    page.get_by_label("Пароль").click()
    page.get_by_label("Пароль").type("89087814701", delay=50)
    page.get_by_role("button", name="Войти", exact=True).click()
    page.wait_for_url("**/app/advertiser/campaigns", timeout=15000)
    return page
