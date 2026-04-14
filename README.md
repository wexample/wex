# wex

Version: 6.0.0

## Table of Contents

- [Introduction](#introduction)
- [Testing](#testing)

## Check Wex Installation

Test if the core command works using these methods:

```bash
# Once installed globally
wex hi  # Returns "hi!"

# From wex directory (no global install required)
bash bin/wex hi  # Returns "hi!"
```

### Using Command

Execute all tests including core and every addon tests suite.

```bash
# Run all tests with integrated logging
bash bin/wex test::run/all
```

### Using Pytest Directly

Basic command to test only core tests.

```bash
# Run all tests
pytest

# Or using Python module
python -m pytest
```

## Testing

This project uses pytest for unit and integration testing. You can run tests using either the built-in WEX command or
pytest directly.

## Test Structure

```
tests/
├── unit/           # Unit tests (test individual components)
│   └── test_example.py
├── integration/    # Integration tests (test component interactions)
└── conftest.py     # Shared fixtures (create as needed)
```

