# CLAUDE.md — Rizz QA Tests
# Этот файл загружается автоматически каждую сессию. Не читать исходники повторно — всё нужное здесь.

## Проект
- **Платформа:** https://app.rizz.market
- **Стек:** Python + Playwright (sync_api) + Pytest + Allure
- **Оператор:** Губорев Данил Викторович (@danillQaa)
- **Команда запуска:** `pytest -m <marker>` или `pytest tests/test_suites/<suite>/`
- **Allure-отчёт:** `allure serve allure-results`

---

## Учётные данные

### Блогер (creator)
- Телефон (в коде): `9938854791`  (без 7)
- Пароль: `89087814701`
- Storage state: `tests/stage/blogger_state.json`
- Fixture: `blogger_page` → после логина попадает на `MarketPage`

### Рекламодатель (advertiser)
- Телефон (в коде): `79087814701`
- Пароль: `89087814701`
- Storage state: `tests/stage/advertiser_state.json`
- Fixture: `advertiser_page` → после логина попадает на `CampaignsPage`

---

## URL страниц
```
BASE = https://app.rizz.market
SignInPage       = /sign-in
MarketPage       = /app/creator/market
CampaignsPage    = /app/advertiser/campaigns
ProductsPage     = /app/advertiser/products
CreateProductPage= /app/advertiser/products/create
CreateCampaignPage = /app/advertiser/campaigns/create
EditCampaignPage = /app/advertiser/campaigns/<id>/edit
IntegrationPage  = /app/creator/integrations
SendResponsePage = /app/creator/market  (с модалкой отклика)
```

---

## Структура проекта (не Glob-ить повторно)
```
tests/
  conftest.py                  — глобальные fixtures + Allure hooks
  fixtures/
    advertiser_fixture.py      — advertiser_page fixture
    blogger_fixture.py         — blogger_page fixture
    conftest.py
  flows/
    auth_flow.py               — AuthFlow.login_with_phone(phone, password)
  pages/
    base_page.py               — BasePage (visit, navigate, safe_click, safe_fill, expect_*)
    sign_in_page.py
    market_page.py
    campaigns_page.py
    products_page.py
    create_product_page.py
    create_campaign_page.py
    edit_campaign_page.py
    integration_page.py
    send_response_page.py
    cancel_and_reapply_page.py
    campaign_details_page.py
    landing_page.py
  components/
    base_component.py          — BaseComponent(page)
    notification.py
    auth/login_form_component.py
    market_components/
      filter_component.py
      barter_response_component.py
      campaign_card_component.py
  elements/
    base_element.py            — BaseElement
    button.py / input.py / textarea.py / link.py / icon.py / image.py / file_input.py / text.py
  test_data/
    campaign_generator.py
    product_generator.py
  stage/
    generate_auth.py           — скрипт для обновления storage_state файлов
    advertiser_state.json
    blogger_state.json
  test_suites/
    auth/           — test_auth_01..05_*.py
    campaigns/      — test_campaigns_01..04_*.py
    products/       — test_products_01..04_*.py
    responses/
      01_send_response/  — test_responses_01_barter.py, test_responses_02_cancel_and_reapply.py
      02_accept_response/— test_responses_01_process_blogger_response.py
    integrations/
      01_send_media / 02_accept_steps / 03_send_link / 04_accept_steps / 06_signing_act
    filters/        — test_filters_01..03_*.py
    market/         — test_market_01_page_elements.py
    regression_route/ — test_regression_route.py
```

---

## Pytest markers (pytest.ini)
```
authorization   — тесты авторизации
market          — маркет блогера
filters         — фильтрация на маркете
products        — продукты рекламодателя
campaigns       — кампании рекламодателя
responses       — отклики блогера
integrations    — выполнение интеграций
regression      — регрессионные тесты
regress_route   — полный маршрут регресса
```

---

## BasePage — ключевые методы (не читать файл повторно)
```python
page_obj.visit(url?)          # goto URL
page_obj.navigate()           # goto self.URL
page_obj.reload()
page_obj.safe_click(locator)
page_obj.safe_fill(locator, value)
page_obj.wait_for_element(locator, state="visible")
page_obj.wait_for_hidden(locator)
page_obj.wait_for_load(state="domcontentloaded")
page_obj.expect_visible(locator)
page_obj.expect_hidden(locator)
page_obj.expect_url_contains(pattern)
page_obj.expect_heading(name)
page_obj.is_visible(locator)  # → bool
```

---

## Паттерны написания кода

### Новая Page
```python
from tests.pages.base_page import BasePage
import allure
from playwright.sync_api import Page, expect

class MyPage(BasePage):
    URL = "https://app.rizz.market/app/..."

    def __init__(self, page: Page):
        super().__init__(page)
        self.heading = page.get_by_role("heading", name="...")

    @allure.step("Проверка: страница загружена")
    def expect_loaded(self) -> None:
        self.expect_url_contains(r".*/path/")
        expect(self.heading).to_be_visible(timeout=15000)
```

### Новый Component
```python
from tests.components.base_component import BaseComponent
import allure
from playwright.sync_api import Page, expect

class MyComponent(BaseComponent):
    def __init__(self, page: Page):
        super().__init__(page)
        self.root = page.locator(".my-component")

    @allure.step("Действие в компоненте")
    def do_action(self) -> None:
        self.root.get_by_role("button", name="...").click()
```

### Новый тест-файл
```python
import allure
import pytest
from playwright.sync_api import Page

@allure.feature("Feature Name")
@pytest.mark.marker_name
class TestSuiteName:

    @allure.story("Story name")
    @allure.title("Test title")
    def test_01_something(self, advertiser_page: Page) -> None:
        # Arrange
        from tests.pages.campaigns_page import CampaignsPage
        page_obj = CampaignsPage(advertiser_page)
        # Act
        page_obj.click_create()
        # Assert
        page_obj.expect_url_contains(r".*/campaigns/create")
```

### conftest для suite (если нужна shared фикстура)
```python
import pytest
from playwright.sync_api import Page

@pytest.fixture(scope="module")
def shared_state(advertiser_page: Page):
    # setup
    yield {"key": "value"}
    # teardown
```

---

## Ключевые решения / особенности проекта
- Auth через `storage_state` (cookies) — fallback на login_with_phone при протухании
- `pytest.ini`: `--reruns=2 --only-rerun=TimeoutError` — автоматический перезапуск при таймаутах
- `ensure_page_ready_before_test` (autouse) — ждёт `networkidle` перед каждым тестом, timeout=15000ms
- Cookie-баннер "Принять cookie" — кликается в каждой fixture автоматически
- Telegram-уведомление — может появляться на странице, иногда мешает кликам
- `last_product_name.txt` — файл для передачи названия между тест-сессиями (responses suite)
- Нумерация файлов: `test_auth_01_`, `test_auth_02_` — порядок исполнения

---

## Что НЕ делать
- Не Glob-ить весь проект повторно — структура выше актуальна
- Не читать base_page.py / base_component.py — методы описаны выше
- Не читать fixture файлы — credentials и логика выше
- Не читать pytest.ini — markers перечислены выше
