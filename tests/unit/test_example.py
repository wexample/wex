"""
Basic example test to verify pytest setup.
"""

def test_basic_example():
    """A simple test to verify pytest is working."""
    assert 1 + 1 == 2

def test_string_operations():
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
    
    def test_multiplication(self):
        """Test multiplication operation."""
        assert 2 * 3 == 6
        
    def test_division(self):
        """Test division operation."""
        assert 6 / 3 == 2
        assert 5 / 2 == 2.5
