# wex

Version: 6.0.132

wex runs an entire infrastructure from one command line. It manages
applications and the Docker services behind them, keeps project directories in the shape
they declare, publishes packages, drives servers, databases and monitoring, and puts AI
agents to work on your own codebase.

All of it answers to the same grammar — `wex app::state/rectify`, `wex system::kill/by-port`
— so learning one command teaches you how to read every other. Ask any of them what it
takes with `--help`, and write your own the day the one you need is missing.

## Table of Contents

- [Addons](#addons)
- [Installation](#installation)
- [What the installer changes on your machine](#what-the-installer-changes-on-your-machine)
- [Check Installation](#check-installation)
- [Running a command](#running-a-command)
- [Where commands come from](#where-commands-come-from)
- [Options](#options)
- [Writing your own](#writing-your-own)
- [Uninstall](#uninstall)
- [What the uninstaller removes](#what-the-uninstaller-removes)
- [Additional removals on purge](#additional-removals-on-purge)
- [Testing](#testing)

## Addons

wex implements no command itself. Every feature comes from an addon, and
the list below is the one declared in pyproject.toml — installing
wex installs all of them.

| Addon | Role |
| --- | --- |
| [ai](https://pypi.org/project/wexample-wex-addon-ai/) | AI addon for wex |
| [app](https://pypi.org/project/wexample-wex-addon-app/) | App management with wex |
| [dev-css](https://pypi.org/project/wexample-wex-addon-dev-css/) |  |
| [dev-javascript](https://pypi.org/project/wexample-wex-addon-dev-javascript/) | Python dev addon for wex |
| [dev-php](https://pypi.org/project/wexample-wex-addon-dev-php/) | Python dev addon for wex |
| [dev-python](https://pypi.org/project/wexample-wex-addon-dev-python/) | Python dev addon for wex |
| [filestate](https://pypi.org/project/wexample-wex-addon-filestate/) | App management with wex |
| [master](https://pypi.org/project/wexample-wex-addon-master/) | Master addon for wex — control tower over projects, apps, servers, DNS, packages |
| [package](https://pypi.org/project/wexample-wex-addon-package/) | Package management addon for wex |
| [services-collab](https://pypi.org/project/wexample-wex-addon-services-collab/) | Collaboration services (rocketchat, nextcloud, onlyoffice...) for wex |
| [services-db](https://pypi.org/project/wexample-wex-addon-services-db/) | Database services (mysql, postgres...) for wex |
| [services-monitoring](https://pypi.org/project/wexample-wex-addon-services-monitoring/) | Monitoring services (grafana, matomo...) for wex |
| [services-platform](https://pypi.org/project/wexample-wex-addon-services-platform/) | Platform services (n8n, gitlab, jenkins...) for wex |

Each addon documents its own commands. This repository documents the kernel: how it
boots, how a command string is resolved, and what an addon may contribute.

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

## Running a command

A command is one word made of three parts — the addon, the group and the name:

```bash
wex core::ping/hi        # hi!
wex core::version/get    # 6.0.132
```

The addon prefix is optional when the group and name are unambiguous, so `ping/hi`
resolves to the same command. Every part uses hyphens, never underscores:
`system::process/by-port`, not `by_port`. The kernel rejects the underscore form and
suggests the correct spelling.

Tab-completion is registered by the installer, so pressing `<Tab>` mid-command lists the
matching groups and names.

## Where commands come from

The prefix tells the kernel where to look. Four namespaces coexist:

| Form | Example | Lives in |
| --- | --- | --- |
| `addon::group/command` | `core::ping/hi` | the addon's `commands/` directory |
| `.group/command` | `.deploy/staging` | `.wex/commands/` of the current project |
| `~group/command` | `~test/hello` | `~/.wex/commands/` |
| `@service::group/command` | `@mysql::db/dump` | the matching service addon |

Addon commands are scanned once and cached. Project and user commands are re-read at
every run, so a file you just created is immediately callable.

## Options

Each command declares its own options, with a long and usually a short form. Ask any
command what it takes:

```bash
wex system::process/by-port --help
```

```
Usage: system::process/by-port [OPTIONS]
Return info about the process listening on a port
Options:
  --port, -p  <int>  [required]  Port number
  --help, -h  Show this message and exit.
```

```bash
wex system::process/by-port -p 6543
```

A handful of options are understood by every command, because they are handled by the
kernel rather than by the command:

| Option | Effect |
| --- | --- |
| `--quiet` | silence the interface — progress, prompts, logs |
| `-vv`, `-vvv` | raise verbosity; `-vvv` prints full tracebacks instead of a crash report path |
| `--output-format` | render the response as `str` (default) or `json` |
| `--output-target` | send the response to `stdout`, `file`, or `none` |
| `--output-file` | write the response to a given path, implies `--output-target file` |

`--quiet` silences the interface, not the result: `wex core::ping/hi --quiet` still prints
`hi!`. What a command returns is data, and data is never suppressed by a display flag.

## Writing your own

`core::command/create` scaffolds the file at the right place, in Python or as a YAML
workflow:

```bash
wex core::command/create --command "~notes/open" --extension py
```

The file path and the function name are both the command address, spelled differently:
`~notes/open` becomes `~/.wex/commands/notes/open.py` holding a `user__notes__open()`
function. There is no registration step — the resolver finds it by scanning.

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
