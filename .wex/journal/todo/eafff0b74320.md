# Nettoyage des issues GitLab — wexample/wex

## Context

15 open issues since 2023 on https://gitlab.wexample.com/wexample/wex.
All date from the v5 era (wexd, bash). Goal: zero open issues.

## API Access

- Token stored in `.wex/.env` → `GITLAB_API_TOKEN`
- Base URL: `https://gitlab.wexample.com/api/v4`
- Project: `wexample%2Fwex`

Read an issue:
```
curl -s --header "PRIVATE-TOKEN: $GITLAB_API_TOKEN" "$GITLAB_API_URL/projects/wexample%2Fwex/issues/<iid>"
```

Close an issue:
```
curl -s -X PUT --header "PRIVATE-TOKEN: $GITLAB_API_TOKEN" \
  "$GITLAB_API_URL/projects/wexample%2Fwex/issues/<iid>" \
  --data "state_event=close"
```

## Procedure per issue

1. Read the full description
2. Challenge: still relevant? already done? obsolete?
3. If relevant → implement or create a dedicated roadmap, then close
4. If obsolete → close directly
5. Check off below

## Issues (chronological order)

- [x] #1 — Wexd (2023-05-11)
- [x] #2 — Wexd logs (2023-05-12)
- [x] #6 — Wexd limit number of arguments (2023-05-27)
- [x] #7 — Webhook python (2023-06-05)
- [x] #8 — wex default::context/find (2023-06-07)
- [x] #9 — Issue with Docker volumes pointing to a file (2023-06-11)
- [x] #10 — Fix install (2023-10-24)
- [x] #11 — Prod deployment (2023-10-24)
- [x] #12 — Test services (2023-10-26)
- [ ] #13 — Display pass (2023-10-26)
- [ ] #14 — my.cnf disable log bin (2023-10-30)
- [ ] #15 — Ability to dump / restore a different database name (2023-10-30)
- [ ] #16 — WP update in yml format (2023-10-30)
- [ ] #17 — Use local debian directories (2023-10-30)
- [ ] #18 — Deployment bugs (2023-11-16)
