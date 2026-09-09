## Output — prompts vs logs vs responses

### Three distinct concerns

| | Prompt | Log | Response |
|---|---|---|---|
| **Recipient** | Human at terminal | System / ops | Data consumer |
| **Mechanism** | `context.io.*` (wexample-prompt) | `kernel.logger` (Python logging) | Response types (`DictResponse`, …) |
| **Destination** | stdout / tty | stderr / file / aggregator | stdout (`str` or `json` format) |
| **Silenceable** | Yes (`--quiet`, `output_target=none`) | No (survives `--quiet`) | Yes (`output_target=none`) |

### Decision rule

> *"If an ops engineer or a script needs to read it, it's a log. If it's for a human typing at the terminal, it's a prompt."*

### Container / service case

When wex runs inside a Docker container or as a systemd service:
- **Prompts** can be silenced — intentionally, nobody reads them
- **Logs** are always captured (`docker logs`, journald, etc.) — that is what they are for
- **Responses** in `json` are usable by scripts that call wex

### Exemples

```python
# ✅ Prompt — intended for humans
context.io.log("Building registry...")
context.io.success("Done.")

# ✅ Log — intended for the system
kernel.logger.info("Registry hydrated in 0.3s")
kernel.logger.warning("Service config not found, using defaults")
kernel.logger.debug("Resolver chain: addon → service → user")

# ❌ Do not use logger for user feedback
kernel.logger.info("Starting app...")  # silent in prod, humans will not see it

# ❌ Do not use io for technical diagnostics
context.io.log(f"Registry keys: {list(registry.keys())}")  # noise for humans
```

### Log levels by verbosity

| Flag | `VerbosityLevel` | `logging` level |
|---|---|---|
| `--quiet` | QUIET | CRITICAL |
| _(default)_ | DEFAULT | WARNING |
| `--v` | MEDIUM | INFO |
| `--vv` | HIGH | INFO |
| `--vvv` | MAXIMUM | DEBUG |
