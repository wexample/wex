# Kernel

## v5 reference

- Entry: `wex-5/__main__.py` → `Kernel().call()`
- Kernel: `wex-5/src/utils/kernel.py`

## Features

- [x] Verbosity levels: `quiet` / `default` / `medium` / `maximum` — `VerbosityLevel` enum in `prompt` package
- [x] Render modes / output handlers: `stdout` / `file` / `none` — pluggable output targets in wex-core
- [x] Addon and command resolution orchestration — `Kernel` in wex-core
- [x] Addon registration system — `AbstractAddonManager` + addon registry
- [x] SKIP Task ID generation (format: `YYYYMMDD-HHMMSS-nanoseconds-PID`) — bash-side, to verify in `bin/wex`
- [x] SKIP Post-exec command handling (bash-side loop after Python exits)

## v6 target

- `wex-core` → `Kernel` (extends `CommandRunnerKernel`, `CommandLineKernel`, `AbstractKernel`)
