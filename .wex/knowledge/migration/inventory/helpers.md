# Helpers

## Principle

- We do not migrate v5 helpers one by one by default.
- Useless or dead helpers are dropped.
- Generic helpers are dispatched into shared packages (`packages/helpers`, `packages/prompt`, `packages/filestate`, etc.).
- Wex-specific helpers stay only when they still carry Wex-specific behavior (`wex-core`, addon helpers).

## Quick status

- Most former `wex-5/src/helper/*` material is already absorbed by the Python packages layout.
- This inventory is intentionally lightweight: if a helper still matters, it should show up through a real command, workdir, service, or package need.

## Still worth checking case by case

- `core.py`
  Core-only helper behavior may belong in `wex-core`.
- `service.py`
  Only if a remaining service flow still needs explicit helper logic.
- `routing.py`
  Only if webhook / routing migration needs old route helpers.
- `test.py`
  Only if old test-generation behavior is still wanted.
- addon-specific helpers
  Keep only when the logic is truly addon-specific and not generic enough for shared packages.

## Not tracked in detail anymore

- `command.py`
- `string.py`
- `file.py`
- `prompt.py`
- `user.py`
- `module.py`
- `package.py`
- `patch.py`
- `process.py`
- `registry.py`
- `system.py`

These are considered either already redistributed, superseded, or not worth migrating as a dedicated v5 helper list.

## v6 target

- Generic helpers → `PACKAGES/PYTHON/packages/helpers`
- Prompt helpers → `PACKAGES/PYTHON/packages/prompt`
- File / state helpers → `PACKAGES/PYTHON/packages/filestate`
- Wex-specific helpers → `PACKAGES/PYTHON/wex/wex-core`
