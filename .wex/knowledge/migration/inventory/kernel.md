# Kernel

## v5 reference

- Entry: `wex-5/__main__.py` → `Kernel().call()`
- Kernel: `wex-5/src/utils/kernel.py`

## Features

- [ ] Task ID generation (format: `YYYYMMDD-HHMMSS-nanoseconds-PID`)
- [ ] Post-exec command handling (bash-side loop after Python exits)
- [ ] Verbosity levels: `quiet` / `default` / `medium` / `maximum`
- [ ] Render modes: `terminal` / `json` / `none`
- [ ] Addon and command resolution orchestration
- [ ] Response rendering pipeline

## v6 target

- `wex-core` → `AbstractKernel`
