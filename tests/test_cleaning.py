import pytest

from market_calendar_tool.cleaning.cleaner import (
    ImpactLevel,
    camel_to_snake,
    impact_mapping,
    is_valid_currency,
)


@pytest.fixture
def impact_level_enum():
    return ImpactLevel


@pytest.fixture
def impact_mapping_fixture():
    return impact_mapping


def test_is_valid_currency():
    assert is_valid_currency("USD")
    assert is_valid_currency("EUR")
    assert not is_valid_currency("ABC")
    assert is_valid_currency("all")
    assert not is_valid_currency("")
    assert not is_valid_currency(None)


def test_camel_to_snake():
    assert camel_to_snake("camelCase") == "camel_case"
    assert camel_to_snake("CamelCaseTest") == "camel_case_test"
    assert camel_to_snake("test") == "test"
    assert camel_to_snake("TestHTTPResponse") == "test_http_response"
    assert camel_to_snake("") == ""
    assert camel_to_snake("aB") == "a_b"
