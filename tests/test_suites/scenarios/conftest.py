"""Фикстуры для сценарных тестов.

Используют общие фикстуры из корневого conftest.py:
- advertiser_page
- created_product
- created_campaign
"""
import pytest


@pytest.fixture(scope="session")
def browser_context_args():
    return {
        "no_viewport": True,
        "locale": "ru-RU",
    }


@pytest.fixture(scope="session")
def browser_type_launch_args():
    return {
        "args": ["--start-maximized"],
        "headless": False,
    }
