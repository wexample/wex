# Virtual Environments

You are reading this file because you want information about the project specific virtual environment management.

## Rules
- Main venv: `.wex/python/venv`
- Package-specific venv: `{package}/.wex/venv`
    - Development: Local packages installed with `-e`
    - Testing: Normal installation except current package
