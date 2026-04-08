# Addon: services-db

## v5 reference

`wex-5/addons/services_db/`

## v6 target

- Dedicated `PACKAGES/PYTHON/wex/wex-addon-services-db`

## Status

- [x] Dedicated `wex-addon-services-db` package in place for DB services
- [x] `mysql`
- [x] `postgres`
- [x] `mongo`
- [x] `maria`
- [x] `redis`
- [x] `sqlserver`

## Notes

- The functional service surface is now present in v6 for the main database family.
- Some old v5 `app/*` hooks were intentionally not reintroduced automatically in v6 when no clean hook mechanism existed yet.
- Remaining DB-related migration work is now tracked separately in [todo/addons/db.md](../todo/addons/db.md) for `remote/push_restore`.
