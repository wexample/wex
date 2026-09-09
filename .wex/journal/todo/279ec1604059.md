# Erreurs subprocess — chaîne A → B → C

## Context

```
A (wex package::suite/publish)
  → shell_run(.wex/bin/app-manager app::package/push)   # B
      → shell_run(git push -u origin ...)                           # C — root cause
```

Current result: B has already displayed its error. A re-displays a `ShellCommandFailedException`
on subprocess B, which either duplicates the message or buries it.

## What is done

- `ShellCommandFailedException` propagated from C up to A ✅
- `exec_argv()` displays a clean message + "To retry manually" ✅

## What remains

### Detect that a subprocess is a wex

- [ ] Create `shell_is_wex_subprocess(cmd) -> bool` in `helpers/shell.py`
  — checks whether `.wex/bin/app-manager` or `bin/wex` is in the args

### Silence the re-display on A's side

- [ ] When A receives a `ShellCommandFailedException` for a detected wex subprocess,
  display only: `[SUB_PROCESS_FAILED] <commande> — see above.` without repeating the detail
- [ ] If the subprocess is not wex (e.g. direct git) → current behaviour unchanged

## Target output (A→B→C)

```
[SHELL_COMMAND_FAILED] Command exited with code 128
  Command : git push -u origin version-0.3.11
  Stderr  : error: src refspec version-0.3.11 does not match any

To retry manually:
  git push -u origin version-0.3.11
```

C's error is what gets displayed. Layers B and A do not repeat it.
