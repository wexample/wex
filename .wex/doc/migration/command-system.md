# Command System Migration

You are reading this file because you need to understand the command system migration from v5 to v6.

## Current System (v5)

The v5 command system is implemented in `/home/weeger/Desktop/WIP/WEB/WEXAMPLE/WEX/local/wex/src/utils/kernel.py` with the following characteristics:

- Command resolution through multiple resolvers
- Extensive use of decorators for command properties:
  - `@command` and `@test_command` for command definition
  - `@alias`, `@attach`, `@as_sudo`, `@no_log`, `@verbosity` for properties
- Addon-based architecture with dynamic loading
- Registry-based command management
- Support for different command types and rendering modes

## New System (v6)

### Entry Point
- Located at `__main__.py`
- Uses `exec_argv()` for command detection and execution
- Currently in development phase

### Command Detection System
1. **Architecture**:
   - Commands are handled through command resolvers
   - Resolvers are initialized in `AbstractKernel._init_resolvers()`
   - Each resolver should implement `AbstractCommandResolver`

2. **Current Issue**:
   - Command list is empty because no resolvers are registered
   - `_build_command_requests_from_arguments` returns an empty list
   - No command resolver implementation found in wex-core

3. **Testing**:
   - `cli/wex` Should not fail
