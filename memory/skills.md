# Skills — Готовые сниппеты для типовых операций
# Читать когда нужно написать типовой код — не изобретать заново

## 1. Обновить storage_state (протухла авторизация)
```bash
cd /Users/mbookpro403gmail.com/Documents/QA/rizz-qa-tests
python tests/stage/generate_auth.py
```

## 2. Запуск конкретного suite
```bash
pytest -m authorization
pytest -m campaigns
pytest -m products
pytest -m responses
pytest -m integrations
pytest -m filters
pytest -m market
pytest tests/test_suites/regression_route/
```

## 3. Запуск одного теста
```bash
pytest tests/test_suites/campaigns/test_campaigns_01_create_empty.py -v
```

## 4. Открыть Allure-отчёт
```bash
allure serve allure-results
```

## 5. Шаблон conftest для suite с shared advertiser session
```python
import pytest
from playwright.sync_api import Page
from tests.pages.campaigns_page import CampaignsPage

@pytest.fixture(scope="module")
def campaign_data(advertiser_page: Page):
    """Создать кампанию один раз на весь модуль."""
    # ... setup ...
    yield {"campaign_id": "..."}
    # ... teardown / cleanup ...
```

## 6. Шаблон conftest с двумя ролями (advertiser + blogger)
```python
# В тесте используй две разные страницы через BrowserContext
# Blogger и advertiser должны быть в разных context-ах
# Playwright pytest-plugin создаёт отдельный context для каждой фикстуры
```

## 7. Шаблон теста на создание сущности
```python
def test_01_create_entity(self, advertiser_page: Page) -> None:
    from tests.pages.create_campaign_page import CreateCampaignPage
    from tests.pages.campaigns_page import CampaignsPage

    campaigns = CampaignsPage(advertiser_page)
    campaigns.click_create()

    create = CreateCampaignPage(advertiser_page)
    create.fill_title("Test Campaign")
    create.submit()

    campaigns.navigate()
    campaigns.expect_loaded()
```

## 8. Шаблон теста с Allure-шагами вручную
```python
import allure

def test_something(self, advertiser_page: Page) -> None:
    with allure.step("Открыть страницу"):
        page_obj = SomePage(advertiser_page)
        page_obj.navigate()

    with allure.step("Выполнить действие"):
        page_obj.click_something()

    with allure.step("Проверить результат"):
        page_obj.expect_loaded()
```

## 9. Шаблон параметризованного теста
```python
@pytest.mark.parametrize("phone,password,error", [
    ("1234567890", "wrong", "Неверный пароль"),
    ("0000000000", "pass", "Пользователь не найден"),
])
def test_invalid_login(self, page: Page, phone, password, error) -> None:
    from tests.flows.auth_flow import AuthFlow
    AuthFlow(page).login_expect_error(phone, password, error)
```

## 10. Cleanup после теста (teardown через yield-fixture)
```python
@pytest.fixture()
def created_campaign(advertiser_page: Page):
    # Setup: создаём кампанию
    name = campaign_generator.generate_name()
    # ... create via UI ...
    yield name
    # Teardown: удаляем через API или UI
    # ... delete ...
```

## 11. Работа с file_input (загрузка файла)
```python
# В page объекте
self.file_input = page.locator("input[type='file']")

# В тесте
page_obj.file_input.set_input_files("/path/to/file.jpg")
```

## 12. Ожидание Toast / уведомления
```python
from tests.components.notification import Notification
notification = Notification(page)
notification.check_visible_error("Текст ошибки")
# или
notification.check_visible_success("Успешно")
```

## 13. Работа с dropdown / select
```python
# Паттерн из проекта: click → wait for options → click option
page.get_by_role("combobox").click()
page.get_by_role("option", name="Нужный вариант", exact=True).click()
```

## 14. Нестабильный локатор — fallback подход
```python
# Если один локатор не стабилен — пробуем несколько
def _find_dropdown(self) -> Locator:
    candidates = [
        self.page.locator("[data-testid='dropdown']"),
        self.page.get_by_role("combobox").first,
        self.page.locator(".dropdown-trigger"),
    ]
    for loc in candidates:
        if loc.is_visible(timeout=2000):
            return loc
    raise ValueError("Dropdown не найден ни одним из локаторов")
```

## 15. Сохранение данных между тестами в suite
```python
# Через файл (паттерн проекта)
from pathlib import Path
STATE_FILE = Path(__file__).parent / "last_campaign_title.txt"

# Запись
STATE_FILE.write_text(campaign_name, encoding="utf-8")

# Чтение
campaign_name = STATE_FILE.read_text(encoding="utf-8").strip()
```
