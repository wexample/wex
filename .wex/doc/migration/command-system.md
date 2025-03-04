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

### Addon Commands Implementation

#### Command Format
Addon commands follow the format: `addon::group/command`, for example:
- `default::info/show`

#### Addon Locations
Addons are stored in specific locations within packages:
1. Core addons: `/home/weeger/Desktop/WIP/WEB/WEXAMPLE/PIP/pip/wex-core/wexample_wex_core/addons`
2. Additional addons (future): `/home/weeger/Desktop/WIP/WEB/WEXAMPLE/PIP/pip/wex-addon-app/wexample_wex_addon_app/addons`

#### Command Resolution Process
The addon resolver should:
1. Parse the command format (e.g., `default::info/show`)
2. Locate the corresponding Python file (e.g., `addons/default/instructions/info/show.py`)
3. Convert command path to method name (e.g., `default__info__show`)
4. Execute the method

#### Reference Implementation
The v5 implementation in `/home/weeger/Desktop/WIP/WEB/WEXAMPLE/WEX/local/wex-5/src/core/command/resolver/AddonCommandResolver.py` provides a reference for:
- Command path resolution
- Method name conversion
- Execution flow
