## Addons

wex implements no command itself. Every feature comes from an addon, and
the list below is the one declared in pyproject.toml — installing
wex installs all of them.

| Addon | Role |
| --- | --- |
| [ai](https://pypi.org/project/wexample-wex-addon-ai/) | AI addon for wex |
| [app](https://pypi.org/project/wexample-wex-addon-app/) | App management with wex |
| [dev-css](https://pypi.org/project/wexample-wex-addon-dev-css/) |  |
| [dev-javascript](https://pypi.org/project/wexample-wex-addon-dev-javascript/) | Python dev addon for wex |
| [dev-php](https://pypi.org/project/wexample-wex-addon-dev-php/) | Python dev addon for wex |
| [dev-python](https://pypi.org/project/wexample-wex-addon-dev-python/) | Python dev addon for wex |
| [filestate](https://pypi.org/project/wexample-wex-addon-filestate/) | App management with wex |
| [master](https://pypi.org/project/wexample-wex-addon-master/) | Master addon for wex — control tower over projects, apps, servers, DNS, packages |
| [package](https://pypi.org/project/wexample-wex-addon-package/) | Package management addon for wex |
| [services-collab](https://pypi.org/project/wexample-wex-addon-services-collab/) | Collaboration services (rocketchat, nextcloud, onlyoffice...) for wex |
| [services-db](https://pypi.org/project/wexample-wex-addon-services-db/) | Database services (mysql, postgres...) for wex |
| [services-monitoring](https://pypi.org/project/wexample-wex-addon-services-monitoring/) | Monitoring services (grafana, matomo...) for wex |
| [services-platform](https://pypi.org/project/wexample-wex-addon-services-platform/) | Platform services (n8n, gitlab, jenkins...) for wex |

Each addon documents its own commands. This repository documents the kernel: how it
boots, how a command string is resolved, and what an addon may contribute.
