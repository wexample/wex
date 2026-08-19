# wex

Version: 6.0.129

## Table of Contents

- [Installation](#installation)
- [Check Installation](#check-installation)
- [Testing](#testing)

## Installation

Install wex globally. The script installs the apt requirements, creates
the virtual environment and registers the `wex` command:

```bash
sudo bash bin/install
```

To work on wex itself, overlay the local sources in editable mode. This
keeps the existing virtual environment and does not touch third-party
dependencies:

```bash
bash bin/install-dev
```

To remove it:

```bash
sudo bash bin/uninstall
```

## Check Installation

Test if the core command works using these methods:

```bash
# Once installed globally
wex hi  # Returns "hi!"

# From wex directory (no global install required)
bash bin/wex hi  # Returns "hi!"
```

## Testing

This project uses pytest for unit and integration testing. You can run tests using either the built-in WEX command or
pytest directly.

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

### Test Structure

```
tests/
├── unit/           # Unit tests (test individual components)
│   └── test_example.py
├── integration/    # Integration tests (test component interactions)
└── conftest.py     # Shared fixtures (create as needed)
```
