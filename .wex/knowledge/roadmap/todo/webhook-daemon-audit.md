# Webhook daemon — audit et complétion wex6

## Références

- Wex 5 legacy (monolithe bash) : `/home/weeger/Desktop/WIP/WEB/WEXAMPLE/WEX/local/wex-5-legacy`
  - Commandes webhook wex5 : `addons/app/command/webhook/` (exec, listen, stop, status)
- Wex 6 (Python, packages séparés) :
  - Core daemon : `wex-core/src/wexample_wex_core/addons/core/commands/webhook/`
  - Module webhook : `wex-core/src/wexample_wex_core/webhook/` (handler, routing, const)
  - Décorateur : `wex-core/src/wexample_wex_core/decorator/webhook.py`
  - Addon app : `wex-addon-app/src/wexample_wex_addon_app/`

## État actuel wex6

### Ce qui existe
- `core::webhook/listen` — démarre le daemon (sync/async, --force, --dry-run, --port)
- `core::webhook/stop` — arrête par port
- `core::webhook/status` — statut process + dernières entrées de log
- `core::webhook/exec` — dispatcher interne URL → commande wex
- Handler HTTP threaded avec validation token par HMAC
- Token stocké dans `.wex/local/webhook_tokens.yml` par commande
- Token transmissible via `Authorization: Bearer <token>` ou `?_token=`
- Décorateur `@webhook()` pour marquer une commande comme accessible

### Ce qui manque
- **Aucune commande pour gérer les tokens** : le décorateur mentionne `wex webhook/token-show`
  mais cette commande n'existe pas
- **addon/service webhooks non authifiés** : `_validate_token` retourne `False` pour tout
  ce qui n'est pas `app` (TODO explicite dans le code)
- **Pas d'introspection** : pas de moyen de lister quelles commandes sont `@webhook()`
  pour une app donnée
- **Pas d'installation système** : le daemon n'est pas géré comme service systemd,
  pas d'auto-start ni d'uninstall propre

## Phase 1 — Gestion des tokens

- [ ] `core::webhook/token-generate --command <cmd>` — génère et stocke un token dans
  `.wex/local/webhook_tokens.yml` pour une commande donnée
- [ ] `core::webhook/token-show --command <cmd>` — affiche le token existant
- [ ] `core::webhook/token-list` — liste toutes les commandes avec token enregistré
  pour l'app courante
- [ ] `core::webhook/token-revoke --command <cmd>` — supprime le token

## Phase 2 — Introspection app

- [ ] `app webhook/status` (depuis le workdir de l'app) — affiche :
  - statut du daemon global (port, pid, uptime)
  - liste des commandes `@webhook()` disponibles dans l'app
  - tokens enregistrés pour cette app (masqués sauf préfixe)
- [ ] `core::webhook/list` — liste toutes les commandes marquées `@webhook()`
  dans les addons chargés

## Phase 3 — Authentification addon/service

- [ ] Étendre `_validate_token` pour supporter les webhooks `addon` et `service`
  (token stocké hors app, probablement dans le workdir wex global)

## Phase 4 — Installation système

- [ ] `core::webhook/install` — installe le daemon comme service systemd
  (génère un unit file, `systemctl enable`, `systemctl start`)
- [ ] `core::webhook/uninstall` — désactive et supprime le service
- [ ] Vérifier que `wex app/setup` appelle install si des commandes `@webhook()` sont détectées

## Questions ouvertes

- Le daemon tourne-t-il bien en prod ? Quel port ? Quelle app déclenche les webhooks ?
- Les tokens de prod sont-ils dans `.wex/local/webhook_tokens.yml` sur le serveur ?
- Faut-il un secret partagé global ou un token par commande (actuel) ?
