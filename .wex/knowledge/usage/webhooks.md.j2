## Webhook System

Exposes wex commands over HTTP to trigger them from a CI/CD pipeline, a remote server,
or any tool that can issue a GET request.

**URL pattern:** `http://host:6543/webhook/{type}/{path}?_token=<token>&arg=val`

---

### Quick start

#### 1. Start the daemon

```bash
# In the background
wex core::webhook/listen --async

# In the foreground (for debugging)
wex core::webhook/listen

# Force restart if the port is already in use
wex core::webhook/listen --async --force

# Custom timeout (default 300s, 0 = no limit)
wex core::webhook/listen --worker-timeout 600
```

#### 2. Check that the daemon is running

```bash
wex core::webhook/status

# Directly via HTTP — no auth on /health
curl http://localhost:6543/health
# → {"status": "ok", "uptime_seconds": 42}
```

#### 3. Stop the daemon

```bash
wex core::webhook/stop
```

---

### Supported URL types

| Type | URL | Command executed |
|------|-----|------------------|
| `app` | `/webhook/app/{env}/{app}/{cmd}` | `.{cmd}` in `/var/www/{env}/{app}` |
| `addon` | `/webhook/addon/{addon}/{cmd}` | `{addon}::{cmd}` |
| `service` | `/webhook/service/{service}/{cmd}` | `@{service}::{cmd}` |

---

### Type `app` — commands inside an application

#### Mark a command as accessible

YAML :
```yaml
# .wex/commands/release/deploy.yml
decorators:
  - name: webhook
scripts:
  ...
```

Python :
```python
from wexample_wex_core.decorator.webhook import webhook

@webhook()
@command(type=COMMAND_TYPE_ADDON, description="...")
def my__group__command(context: ExecutionContext) -> None:
    ...
```

#### Manage tokens (from the app workdir)

```bash
# Generate a token for a command
wex app::webhook/token-generate --command-name .release/deploy

# Generate for all @webhook commands of the app at once
wex app::webhook/token-generate --all

# Regenerate (overwrite the existing one)
wex app::webhook/token-generate --command-name .release/deploy --force

# View the full token for a command
wex app::webhook/token-show --command-name .release/deploy

# List all registered tokens (prefix only)
wex app::webhook/token-list

# Revoke a token
wex app::webhook/token-revoke --command-name .release/deploy

# Revoke all tokens for the app
wex app::webhook/token-revoke --all
```

Tokens are stored in `{app_path}/.wex/local/webhook_tokens.yml`.

#### App webhook status

```bash
wex app::webhook/status
```

Shows: daemon state, number of `@webhook` commands, number of tokens present.
This summary also appears in `wex app::info/show`.

#### Call the webhook

```bash
# Token as query param
curl "http://localhost:6543/webhook/app/prod/myapp/release/deploy?_token=<token>"

# Token as header
curl -H "Authorization: Bearer <token>" \
     "http://localhost:6543/webhook/app/prod/myapp/release/deploy"

# With arguments passed to the command
curl "http://localhost:6543/webhook/app/prod/myapp/release/deploy?_token=<token>&version=1.2.3"

# Force synchronous execution (waits for completion, returns output)
curl "http://...?_token=<token>&_async=0"
```

---

### Type `addon` — global addon commands

#### Manage tokens

```bash
# Generate a token for an addon command
wex core::webhook/token-generate --type addon --command-name app::info/show

# Generate for all @webhook addon commands
wex core::webhook/token-generate --type addon --all

# --force, --all, token-show, token-list, token-revoke: same options as for app
wex core::webhook/token-show   --type addon --command-name app::info/show
wex core::webhook/token-list   --type addon
wex core::webhook/token-revoke --type addon --command-name app::info/show
wex core::webhook/token-revoke --type addon --all
```

Tokens are stored in `{wex_workdir}/.wex/local/webhook_tokens_addon.yml`.

#### Appeler le webhook

```bash
curl "http://localhost:6543/webhook/addon/app/info/show?_token=<token>"
```

---

### Type `service` — service commands

Identical to the `addon` type, replace `--type addon` with `--type service`.

Tokens stored in `{wex_workdir}/.wex/local/webhook_tokens_service.yml`.

```bash
curl "http://localhost:6543/webhook/service/nginx/status?_token=<token>"
```

---

### Observability

#### Logs

```bash
# Latest requests (20 by default)
wex core::webhook/status

# Raw log — JSON, one line per request
tail -f {wex_workdir}/logs/webhook.log
```

Fields: `ts`, `ip`, `path`, `command_type`, `command_path`, `status`, `duration_ms`, `pid`.
Rotation: 5 files × 1 MB max.

#### Prometheus metrics

```bash
curl http://localhost:6543/metrics
```

Exposes (without authentication):
- `webhook_requests_total{command_type, status}` — counter by type and status
- `webhook_request_duration_seconds_sum{command_type}` — cumulative duration
- `webhook_request_duration_seconds_count{command_type}` — number of measured requests

---

### Security

- Token transmitted via `Authorization: Bearer <token>` or `?_token=<token>`
- Constant-time comparison (`hmac.compare_digest`)
- Missing or invalid token → **401**, logged with IP + path
- `/health` and `/metrics` are exempt from authentication

---

### Architecture

#### Separation of concerns

```
wex-core       →  HTTP daemon, generic routing, HMAC validation, addon/service resolvers
wex-addon-app  →  AppWebhookTypeResolver, app::webhook/* commands
```

#### Type resolvers (`WebhookTypeResolver` Protocol)

Each URL type delegates to a resolver that implements:

```python
def build_command(command_path: str) -> str | None  # builds the wex command
def resolve_cwd(command_path: str) -> str | None    # working directory of the subprocess
def resolve_token(command_path: str, command_str: str) -> str | None  # reads the expected token
```

Resolvers registered at daemon startup in `listen.py`:

| Type | Class | Token |
|------|-------|-------|
| `app` | `AppWebhookTypeResolver` (wex-addon-app) | `{app}/.wex/local/webhook_tokens.yml` |
| `addon` | `AddonWebhookTypeResolver` (wex-core) | `{wex_workdir}/.wex/local/webhook_tokens_addon.yml` |
| `service` | `ServiceWebhookTypeResolver` (wex-core) | `{wex_workdir}/.wex/local/webhook_tokens_service.yml` |

#### Daemon

| Option | Default | Description |
|--------|---------|-------------|
| `--port` | `6543` | Listening port |
| `--async` | `false` | Starts as a background subprocess |
| `--force` | `false` | Kills the existing process on the port |
| `--worker-timeout` | `300` | Synchronous subprocess timeout in seconds (0 = unlimited) |
| `--dry-run` | `false` | Binds the socket without serving (tests) |

- **SIGTERM** → graceful shutdown: running workers finish before the server closes
- Timeout exceeded → HTTP **504**, process cleanly killed

---

### Command reference

| Command | Role |
|---------|------|
| `core::webhook/listen` | Start the daemon |
| `core::webhook/stop` | Stop the daemon |
| `core::webhook/status` | State + last log lines |
| `core::webhook/exec` | Internal dispatcher (called by the daemon) |
| `core::webhook/token-generate` | Generate an addon/service token |
| `core::webhook/token-show` | Show an addon/service token |
| `core::webhook/token-list` | List addon/service tokens |
| `core::webhook/token-revoke` | Revoke an addon/service token |
| `app::webhook/status` | Webhook status of the current app |
| `app::webhook/token-generate` | Generate a token for an app command |
| `app::webhook/token-show` | Show an app token |
| `app::webhook/token-list` | List app tokens |
| `app::webhook/token-revoke` | Revoke an app token |
