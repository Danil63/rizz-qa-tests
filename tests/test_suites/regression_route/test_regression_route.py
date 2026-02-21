"""Упорядоченный маршрут регресса.

Запускает существующие test_suites в строгом порядке:
    1) auth
    2) products
    3) campaigns
    4) filters

После каждого сьюта выполняется уникальный teardown.

Важно:
- Этот файл НЕ заменяет независимые тесты.
- Каждый тест из test_suites по-прежнему можно запускать отдельно.
"""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import pytest

from tests.test_suites.regression_route.cleanup import (
    teardown_after_auth,
    teardown_after_products,
    teardown_after_campaigns,
    teardown_after_filters,
)


@dataclass(frozen=True)
class SuiteStep:
    name: str
    path: str
    teardown: callable


SUITE_ORDER = [
    SuiteStep("auth", "tests/test_suites/auth", teardown_after_auth),
    SuiteStep("products", "tests/test_suites/products", teardown_after_products),
    SuiteStep("campaigns", "tests/test_suites/campaigns", teardown_after_campaigns),
    SuiteStep("filters", "tests/test_suites/filters", teardown_after_filters),
]


@pytest.mark.regression
@pytest.mark.regress_route
def test_regression_route() -> None:
    """Прогнать полный регресс в фиксированном порядке одной командой."""
    project_root = Path(__file__).resolve().parents[3]

    for step in SUITE_ORDER:
        command = [
            sys.executable,
            "-m",
            "pytest",
            step.path,
            "-v",
            "-s",
        ]
        result = subprocess.run(
            command,
            cwd=project_root,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            pytest.fail(
                f"Suite '{step.name}' failed.\n"
                f"STDOUT:\n{result.stdout}\n"
                f"STDERR:\n{result.stderr}",
                pytrace=False,
            )

        # Уникальный teardown после каждого suite
        step.teardown()
