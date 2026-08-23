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
