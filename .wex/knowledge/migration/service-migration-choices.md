# Service Migration Choices

Notes written after the migration work, to help the final review pass validate whether the chosen tradeoffs were the right ones.

## Choices we made during service migration

- During service migration, we chose to restore functional parity through the v6 declarative structure first: `service.yml`, compose, samples, and only the commands that were still clearly useful.
- During service migration, we chose not to force a 1:1 rewrite of old v5 `app/*` hooks when v6 had no clean execution point for them.
- During service migration, we chose to keep `service/install` focused on service-specific defaults, while global sample installation stayed in the app addon.
- During service migration, we chose to port the useful runtime core and persistent volumes of heavy services, without recopiying every large upstream-derived config file from v5.
- During service migration, we chose to favor explicit service code over a generic command inheritance mechanism when the abstraction started to feel weaker than the duplication.
- During service migration, we chose to store service-specific helper code under `services/<service>/helpers/`.
- During service migration, we chose to build clean usable baselines for `services-db`, `services-platform`, `services-collab`, and `services-monitoring`, while leaving room for a later second pass on production-specific tuning.

## What to verify during the final pass

- Verify that the dropped v5 `app/*` hooks were truly obsolete or safely covered elsewhere in v6.
- Verify that the reduced config surface of heavy services did not hide an important field-tested tweak from v5.
- Verify that each migrated service is operational with its current baseline, not only structurally present.
- Verify that duplicated service commands did not drift where a simpler shared pattern would now be safe.
