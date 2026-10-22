## Testing

This project uses pytest for unit and integration testing. You can run tests using either the built-in WEX command or
pytest directly.

### Using Command

Execute all tests including core and every addon tests suite.

```bash
# Run all tests with integrated logging
bash bin/wex app::test/run
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

`testpaths` is `tests`, and `pythonpath` is `src` — a test imports the kernel as an
installed package would.

```
tests/
├── unit/           # Unit tests (test individual components)
├── resources/      # Files a test reads from
└── samples/        # Fixture projects a test operates on
```
