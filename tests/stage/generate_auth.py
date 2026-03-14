"""Скрипт генерации storage_state для рекламодателя и блогера.

Запуск:
    python tests/stage/generate_auth.py

Создаёт:
    tests/stage/advertiser_state.json
    tests/stage/blogger_state.json
"""

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

# Добавляем корень проекта в sys.path
ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))

from tests.flows.auth_flow import AuthFlow
from tests.pages.campaigns_page import CampaignsPage
from tests.pages.market_page import MarketPage

STAGE_DIR = Path(__file__).parent

ACCOUNTS = [
    {
        "name": "advertiser",
        "phone": "9087814701",
        "password": "89087814701",
        "check_page": "campaigns",
    },
    {
        "name": "blogger",
        "phone": "9938854791",
        "password": "89087814701",
        "check_page": "market",
    },
]


def generate():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=["--start-maximized"])

        for account in ACCOUNTS:
            print(f"🔐 Авторизация: {account['name']}...")
            context = browser.new_context(no_viewport=True, locale="ru-RU")
            page = context.new_page()

            auth = AuthFlow(page)
            auth.login_with_phone(account["phone"], account["password"])

            # Ждём редирект
            if account["check_page"] == "campaigns":
                CampaignsPage(page).expect_loaded()
            else:
                MarketPage(page).expect_loaded()

            # Принимаем cookie
            cookie_btn = page.get_by_role("button", name="Принять cookie")
            if cookie_btn.is_visible(timeout=3000):
                cookie_btn.click()

            # Сохраняем state
            state_file = STAGE_DIR / f"{account['name']}_state.json"
            context.storage_state(path=str(state_file))
            print(f"   ✅ Сохранено: {state_file}")

            page.close()
            context.close()

        browser.close()
        print("\n🎉 Все состояния сгенерированы!")


if __name__ == "__main__":
    generate()
