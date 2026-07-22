import json
from pathlib import Path

import pytest


REPORT_PATH = Path("/app/report.json")


@pytest.fixture(scope="module")
def report() -> dict[str, object]:
    assert REPORT_PATH.is_file(), "Expected /app/report.json to be created"
    try:
        parsed = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        pytest.fail(f"report.json is not valid JSON: {error}")
    assert isinstance(parsed, dict), "report.json must contain a JSON object"
    return parsed


def test_report_schema(report: dict[str, object]) -> None:
    """Success criterion 1: the artifact has the required keys and value types."""
    assert set(report) == {"total_requests", "unique_ips", "top_path"}
    assert type(report["total_requests"]) is int
    assert type(report["unique_ips"]) is int
    assert isinstance(report["top_path"], str)


def test_total_requests(report: dict[str, object]) -> None:
    """Success criterion 2: every non-empty request record is counted."""
    assert report["total_requests"] == 6


def test_unique_ips(report: dict[str, object]) -> None:
    """Success criterion 3: distinct client IP addresses are counted."""
    assert report["unique_ips"] == 3


def test_top_path(report: dict[str, object]) -> None:
    """Success criterion 4: the most frequently requested path is reported."""
    assert report["top_path"] == "/index.html"
