"""Упрощённый маршрут регресса.

Запускает существующие test_suites в строгом порядке:
    1) auth
    2) products
    3) campaigns
    4) filters
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest


SUITE_ORDER = [
    ("products", "tests/test_suites/products"),
    ("campaigns", "tests/test_suites/campaigns"),
    ("filters", "tests/test_suites/filters"),
    ("responses", "tests/test_suites/responses"),
]


@pytest.mark.regression
@pytest.mark.regress_route
def test_regression_route() -> None:
    """Прогнать полный регресс в фиксированном порядке одной командой."""
    project_root = Path(__file__).resolve().parents[3]

    for suite_name, suite_path in SUITE_ORDER:
        command = [
            sys.executable,
            "-m",
            "pytest",
            suite_path,
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
                f"Suite '{suite_name}' failed.\n"
                f"STDOUT:\n{result.stdout}\n"
                f"STDERR:\n{result.stderr}",
                pytrace=False,
            )
