# Helpers

## Audit Verdict

- No blocking helper-by-helper migration lane remains for a functionally complete v6.
- Former v5 helpers are already redistributed across shared packages, addon code, or `wex-core`.
- Any future helper work should be reopened only from a concrete missing feature, not from helper parity alone.

## Redistribution

- Generic helpers -> `PACKAGES/PYTHON/packages/helpers`
- Prompt / verbosity helpers -> `PACKAGES/PYTHON/packages/prompt`
- File / state helpers -> `PACKAGES/PYTHON/packages/file` and `PACKAGES/PYTHON/packages/filestate`
- Wex-specific glue -> `PACKAGES/PYTHON/wex/wex-core`

## Remaining Watchpoints

- Old `service.py` / `routing.py` behavior is now tracked through addon and webhook inventories, not as a helper backlog.
- Old `test.py` generation helpers stay out of scope with the current "tests excluded" rule.

## Conclusion

This domain is considered closed for migration tracking.
