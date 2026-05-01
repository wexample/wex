# Nettoyage des issues GitLab — wexample/wex

## Contexte

15 issues ouvertes depuis 2023 sur https://gitlab.wexample.com/wexample/wex.
Toutes datent de l'époque v5 (wexd, bash). Objectif : zéro issue ouverte.

## Accès API

- Token stocké dans `.wex/.env` → `GITLAB_API_TOKEN`
- Base URL : `https://gitlab.wexample.com/api/v4`
- Projet : `wexample%2Fwex`

Lire une issue :
```
curl -s --header "PRIVATE-TOKEN: $GITLAB_API_TOKEN" "$GITLAB_API_URL/projects/wexample%2Fwex/issues/<iid>"
```

Fermer une issue :
```
curl -s -X PUT --header "PRIVATE-TOKEN: $GITLAB_API_TOKEN" \
  "$GITLAB_API_URL/projects/wexample%2Fwex/issues/<iid>" \
  --data "state_event=close"
```

## Procédure par issue

1. Lire la description complète
2. Challenger : toujours pertinent ? déjà fait ? obsolète ?
3. Si pertinent → réaliser ou créer une roadmap dédiée, puis fermer
4. Si obsolète → fermer directement
5. Cocher ci-dessous

## Issues (ordre chronologique)

- [x] #1 — Wexd (2023-05-11)
- [ ] #2 — Wexd logs (2023-05-12)
- [ ] #6 — Wexd limiter le nombre d'arguments (2023-05-27)
- [ ] #7 — Webhook python (2023-06-05)
- [ ] #8 — wex default::context/find (2023-06-07)
- [ ] #9 — Souci avec les volumes Docker pointant sur un fichier (2023-06-11)
- [ ] #10 — Fix install (2023-10-24)
- [ ] #11 — Déployment prod (2023-10-24)
- [ ] #12 — Test services (2023-10-26)
- [ ] #13 — Passe display (2023-10-26)
- [ ] #14 — my.cnf disable log bin (2023-10-30)
- [ ] #15 — Pouvoir dump / restor un nom de base différent (2023-10-30)
- [ ] #16 — Mise à jour WP au format yml (2023-10-30)
- [ ] #17 — Utiliser les répertoires locaux de debian (2023-10-30)
- [ ] #18 — Bugs MEP (2023-11-16)
