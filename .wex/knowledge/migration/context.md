# Migration Context

You are reading this file because you need the global context of the v5 → v6 migration.

## Paths

| Role | Path |
|---|---|
| wex-5 (source) | `/home/weeger/Desktop/WIP/WEB/WEXAMPLE/WEX/local/wex-5` |
| wex-6 (target) | `/home/weeger/Desktop/WIP/WEB/WEXAMPLE/WEX/local/wex-6` |
| wex packages | `/home/weeger/Desktop/WIP/WEB/WEXAMPLE/PACKAGES/PYTHON/wex` |
| generic packages | `/home/weeger/Desktop/WIP/WEB/WEXAMPLE/PACKAGES/PYTHON/packages` |

## Key packages

| Package | Path |
|---|---|
| wex-core | `/home/weeger/Desktop/WIP/WEB/WEXAMPLE/PACKAGES/PYTHON/wex/wex-core` |
| wex-addon-app | `/home/weeger/Desktop/WIP/WEB/WEXAMPLE/PACKAGES/PYTHON/wex/wex-addon-app` |
| app | `/home/weeger/Desktop/WIP/WEB/WEXAMPLE/PACKAGES/PYTHON/packages/app` |

## Breaking changes

- Addons are now separated into individual Python pip packages
- Internal "command" components are renamed to "instruction"

## Objectives

- Code quality
- Execution quality
- User interface
- Extensibility
- Overall robustness

## Methodology

1. Compare wex-5 and wex-6 structures
2. Fill the feature inventory in `inventory/`
3. Migrate features domain by domain, with improvements
4. Once a domain is fully migrated, the user removes it from wex-5
5. wex-5 is empty when migration is complete
