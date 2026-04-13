# as_sudo — file ownership preservation

## Problem

When a command decorated with `@as_sudo()` runs, the entire process executes as root.
Any file or directory created during that run (config.yml, .env, workdir dirs, fetched config
files, etc.) ends up owned by `root:root`. The user can no longer edit those files without sudo,
and operations that need a specific non-root uid (e.g. `999:999` for postgres) may also be wrong.

## Root cause

`@as_sudo()` re-executes the process under sudo, which changes the effective uid to 0.
Python's `open()`, `Path.mkdir()`, `shutil.copytree()`, etc. all inherit that uid.
There is no automatic restore of the original user's ownership.

## Available building block

`wexample_helpers.helpers.user.user_get_real_username()` already exists and returns the real
username (via `SUDO_USER` env var) when running under sudo. The companion uid/gid can be
retrieved with `pwd.getpwnam(username)`.

## Roadmap

### Step 1 — Extend the user helper

File: `packages/helpers/src/wexample_helpers/helpers/user.py`

Add two helpers:
- `user_get_real_uid() -> int` — returns `SUDO_UID` (as int) or `os.getuid()`
- `user_get_real_gid() -> int` — returns `SUDO_GID` (as int) or `os.getgid()`

These are the low-level primitives everything else builds on.

### Step 2 — Add a context-aware file creation utility

File: `packages/helpers/src/wexample_helpers/helpers/file.py` (new helpers)

Add:
- `file_write_as_real_user(path: Path, content: str, mode: int = 0o644) -> None`
- `file_mkdir_as_real_user(path: Path, mode: int = 0o755) -> None`

Internally: create/write as root (already have the rights), then `os.chown(path, uid, gid)`
using `user_get_real_uid()` / `user_get_real_gid()`.

### Step 3 — Hook into the as_sudo decorator

File: `wex-core/src/wexample_wex_core/decorator/as_sudo.py`

After the re-executed subprocess returns, the decorator currently just exits.
Instead, expose `SUDO_UID` / `SUDO_GID` / `SUDO_USER` as a typed context accessible
to all code running under the elevated process (e.g. a module-level singleton or a
thread-local set at startup).

This makes the real-user identity available without passing it through every call stack.

### Step 4 — Update workdir/filestate file creation

Files: `wex-addon-app` workdir creation code, `wexample_filestate` item creation operations.

Anywhere a directory or file is created programmatically (not via rectify operations),
replace bare `Path.mkdir()` / `open()` / `write_text()` calls with the helpers from Step 2,
or call `os.chown()` immediately after creation.

Priority locations:
- `app/init.py` — `.wex/`, `.wex/tmp/`, `config.yml`, `.env` creation
- `service/install.py` — samples `shutil.copytree()`
- supabase `install.py` — fetched config files (curl output), `.env` append

### Step 5 — Rectify chown operations

The filestate rectify already handles `owner` specs (e.g. `999:999` on `supabase/db/data`).
Verify that when running as root these operations still target the correct uid/gid from the
spec, not the calling user. This step is likely already correct — just needs a test.

### Step 6 — Validate end-to-end

After a full `app::app/init --services supabase`:
- All files in `.wex/` owned by the real user (`weeger:weeger`)
- `supabase/` dirs owned by real user except `supabase/db/data` → `999:999`
- `git status` shows clean tree
- User can edit `config.yml` and `.env` without sudo
