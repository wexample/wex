# Migration Index

Global dashboard for tracking the v5 -> v6 migration progress.

## Scope

- Goal: identify what still blocks a functionally complete v6.
- Excluded on purpose: unit and functional test migration.

## Read First

- [context.md](context.md) — paths, goals, methodology
- [service-migration-procedure.md](service-migration-procedure.md) — standard procedure for creating addon packages and porting services
- [todo/_index.md](todo/_index.md) — remaining work by domain
- [todo/backlog.md](todo/backlog.md) — condensed actionable backlog
- [done/_index.md](done/_index.md) — migrated or explicitly closed lanes

## Current Picture

- `done/`: kernel, command system, decorators, response system, file structures, helper redistribution, default/system addons, app Docker lifecycle, global Docker quick wins, database service family.
- `todo/`: core mechanisms still open, CLI/autocomplete/install, resource/template gaps, remaining core/app/db/services addon work outside the DB service family.

## Files

- [context.md](context.md) — paths, breaking changes, objectives, methodology
- [done/](done/) — completed or closed domains
- [todo/](todo/) — remaining domains and condensed backlog
