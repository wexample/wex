# Migration to Wex v6

## Context

- Current version: `/home/weeger/Desktop/WIP/WEB/WEXAMPLE/WEX/local/wex`
- New version: `/home/weeger/Desktop/WIP/WEB/WEXAMPLE/WEX/local/wex-6`

## Breaking Changes

Major changes from v5 to v6 include:

- Addons are now separated into individual Python pip packages
- Internal "command" components have been renamed to "instruction"

## Dependencies

The project uses Python packages with the `wexample-*` prefix. These packages are developed locally and can be found in `/home/weeger/Desktop/WIP/WEB/WEXAMPLE/PIP/pip`. Currently, the main dependency is `wexample-wex-core`, which itself has local dependencies.

### Local Development Setup

To install all local packages in development mode, run:
```bash
python /home/weeger/Desktop/WIP/WEB/WEXAMPLE/PIP/pip/.wex/python/script/install_all_packages.py
```
This script will install all local packages in editable mode, allowing for immediate code changes to take effect.

## Current State

The v6 implementation is built on Python using modern practices, with a clear separation between the core functionality (wexample-wex-core v6.0.1) and the CLI interface. The project uses pip-compile for dependency management and includes both standard and development installation scripts. The architecture follows a kernel-based approach, where the main entry point delegates execution to a core kernel component.

## Objectives

Version 6 maintains the same core objectives and main usage as the current version, but aims for overall improvement in the following aspects:

- Code quality
- Execution quality
- User interface
- Extensibility
- Overall program robustness

## Migration Methodology

The migration process follows these steps:

1. Compare directories and files structure between v5 and v6
2. Identify and prioritize core functionalities
3. Migrate core features from v5 to v6 with improvements
4. When possible, backport v6 improvements to v5

This parallel development approach allows for continuous improvement of both versions while ensuring a smooth transition to v6.