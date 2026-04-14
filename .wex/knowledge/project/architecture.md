# Project Architecture

You are reading this file because you need to understand the overall architecture and responsibility distribution in the Wex project.

## Dependency Management

- The core package (`wexample-wex-core`) contains essential functionalities
- Additional features are modularized into separate addons
- The current project manages optional requirements that complement the core functionality
- System compatibility and requirements are handled at the project level, keeping the core focused on business logic

## Core Concept

The project follows a modular architecture with three main components:

- **Installation Manager** (Current Project)
  - Manages Wex installation and system compatibility
  - Handles system-level dependencies
  - Provides the base environment setup

- **Core Logic** (`wexample-wex-core`)
  - Contains the main business logic
  - Implements fundamental features
  - Manages the addon system

- **Addons**
  - Provide additional functionalities
  - Two types of addons:
    - Required: Installed automatically by the core when needed
     - Optional: Defined in the current project for specific use cases
