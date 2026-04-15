"""
Basic example test to verify pytest setup.
"""

from __future__ import annotations


def test_basic_example() -> None:
    """A simple test to verify pytest is working."""
    assert 1 + 1 == 2


def test_string_operations() -> None:
    """Test basic string operations."""
    # String concatenation
    assert "hello" + " " + "world" == "hello world"

    # String methods
    assert "hello world".capitalize() == "Hello world"
    assert "hello world".title() == "Hello World"

    # String formatting
    name = "pytest"
    assert f"Hello, {name}!" == "Hello, pytest!"


class TestGroupedExamples:
    """A test class to demonstrate grouping related tests."""

    def test_division(self) -> None:
        """Test division operation."""
        assert 6 / 3 == 2
        assert 5 / 2 == 2.5

    def test_multiplication(self) -> None:
        """Test multiplication operation."""
        assert 2 * 3 == 6
