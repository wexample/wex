# wex

Version: 6.0.129

## Table of Contents

- [Installation](#installation)
- [What the installer changes on your machine](#what-the-installer-changes-on-your-machine)
- [Check Installation](#check-installation)
- [Uninstall](#uninstall)
- [What the uninstaller removes](#what-the-uninstaller-removes)
- [Additional removals on purge](#additional-removals-on-purge)
- [Testing](#testing)

## Installation

Install wex globally. The script requires Python 3.11 or later to be
installed, creates the virtual environment and registers the `wex` command:

```bash
sudo bash bin/install
```

To work on wex itself, overlay the local sources in editable mode. This
keeps the existing virtual environment, ensures the requirements.txt dependencies are
present, and installs local packages in editable mode without pulling additional
third-party dependencies:

```bash
bash bin/install-dev
```

To remove it:

```bash
sudo bash bin/uninstall
```

## What the installer changes on your machine

- `/usr/local/bin/wex` — symlink to `bin/wex`, makes the `wex` command available system-wide
- `/etc/bash_completion.d/wex` — sources `bin/autocomplete-handler`, enables tab-completion in bash
- `/etc/profile.d/wex.sh` — sources `bin/terminal-handler` at login, activates the shell prompt integration
- `/root/.bashrc` and `/home/<user>/.bashrc` — one line appended (`. /etc/profile.d/wex.sh`) so interactive non-login shells also load the prompt handler

## Check Installation

Test if the core command works using these methods:

```bash
# Once installed globally
wex hi  # Returns "hi!"

# From wex directory (no global install required)
bash bin/wex hi  # Returns "hi!"
```
## Uninstall

Remove the `wex` command and all files the installer placed on your machine:

```bash
sudo bash bin/uninstall
```

To also delete the virtual environment and generated files, pass `purge`:

```bash
sudo bash bin/uninstall purge
```

## What the uninstaller removes

- `/usr/local/bin/wex` — the global symlink
- `/etc/bash_completion.d/wex` — the tab-completion handler
- `/etc/profile.d/wex.sh` — the shell prompt handler
- `/root/.bashrc` and `/home/<user>/.bashrc` — the lines that sourced `/etc/profile.d/wex.sh` or `bin/terminal-handler` directly (dev install)

## Additional removals on purge

Passing `purge` as the first argument removes files that are generated at runtime and
are not touched by a plain uninstall:

- `.venv/` — the Python virtual environment
- `.wex/.env` — the generated environment file
- `tmp/registry.yml` — the generated command registry
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
