# Ticket : Proxy prod failure — wex 6.0.56 / helpers 6.7.0

## Summary

The nginx proxy (`wex-proxy`) in production failed to start after an attempt to install the service via `wex app::service/install -s proxy --force`. This took all the proxied sites offline (16 domains). Resolved manually by restoring a backup.

## Environment

- Server: wexample.com (SSH: `weeger@wexample.com`, key `~/.ssh/id_rsa`)
- Proxy app path: `/var/www/prod/wex-proxy`
- Wex installed at: `/usr/lib/wex/`
- **wex version in production: 6.0.56**
- **`wexample-helpers` version in production: 6.7.0**
- Local `wexample-helpers` version (expected): **6.8.0**

## Timeline of the problem

1. `wex app::app/start` on `/var/www/prod/hat` fails with "no service selected"
2. The `.wex/docker/docker-compose.yml` file is missing from `wex-proxy` — the proxy service was never installed correctly
3. Attempted `wex app::service/install -s proxy --force` → crash:

```
ImportError: cannot import name 'file_copytree_merge_yaml'
from 'wexample_helpers.helpers.file'
(/usr/lib/wex/.venv/lib/python3.12/site-packages/wexample_helpers/helpers/file.py)
```

4. The `file_copytree_merge_yaml` function was added in `wexample-helpers` **6.8.0** and in `wexample-wex-addon-app` during a recent dev session
5. Production still runs on **6.7.0** — the package was not published
6. Vicious circle: proxy down → no GitLab → no CI/CD → no apt → impossible to update wex
7. Emergency resolution: manual copy of the samples from the venv (`/usr/lib/wex/.venv/.../services/proxy/samples/`) to `/var/www/prod/wex-proxy/` over SSH, then `app::app/start`
8. The proxy started but broke the other sites (bad config). Rollback to backup by the user.

## Root cause

The `wexample-helpers` 6.8.0 package (and the associated `wexample-wex-addon-app` dependencies) **were never published on the apt repository** hosted on the server itself. This problem should have been solved before modifying `service/install.py` to import `file_copytree_merge_yaml`.

## What needs to be done

1. **Publish `wexample-helpers` >= 6.8.0** on the server's apt repository
2. **Publish `wexample-wex-addon-app`** in the version that includes `file_copytree_merge_yaml` in `commands/service/install.py`
3. **Update wex on the server** (`apt upgrade wex` or equivalent) to move from 6.0.56 to the current version
4. **Check** that `wex app::service/install -s proxy --force` works on the server after the update
5. **Investigate** why starting the proxy manually broke the other sites (Docker network config?)

## Architectural reminder

The apt repository is hosted on the server itself — any proxy failure cuts off CI/CD and therefore the ability to publish fixes. A continuity plan is needed for this case (documented manual update procedure).
