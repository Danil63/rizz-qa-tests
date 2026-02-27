"""Фикстуры для тестов интеграций."""
import os

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
        "headless": os.getenv("PW_HEADLESS", "0") == "1",
    }
