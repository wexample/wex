# Env management — wex

## Contexte

Trois couches de variables d'environnement coexistent dans wex :

| Fichier | Rôle | Édité par |
|---------|------|-----------|
| `.wex/.env` | Vars de l'app (APP_ENV, credentials services) | L'utilisateur |
| `.wex/local/env.yml` | Vars machine-spécifiques (SSH_AUTH_SOCK, paths locaux). YAML → supporte les valeurs non-string | wex (généré) |
| `.wex/tmp/docker.env` | Merge des deux couches + runtime config aplati. Passé à docker compose via `--env-file` | `app::config/build` |

### Ce qui fonctionne déjà
- `app::env/get` / `set {env}` / `choose` — gestion de APP_ENV
- `core::env/configure` — SSH_AUTH_SOCK → `.wex/local/env.yml`
- `app::config/build` — génère `docker.env` à partir de `.wex/.env` + runtime
- Vars dans `service.yml` (`required`, `default`, `generated`) — promptées au moment de `app::service/install`
- `app_service.get_vars()` — retourne les vars déclarées par un service

---

## Tâches

### 1. Commandes `app::env/var/*`

Permet de lire/écrire des vars individuelles dans `.wex/.env` sans passer par un éditeur.

**Attention :** `app::env/set` existe déjà et prend un seul argument `{environment}` (= APP_ENV).
Les nouvelles commandes vont dans un sous-groupe `var/` pour éviter la collision.

- `app::env/var/list` — affiche le contenu de `.wex/.env` (clé → valeur, une par ligne)
- `app::env/var/set KEY VALUE` — écrit ou écrase une var dans `.wex/.env`
- `app::env/var/get KEY` — lit une var (utile en scripting)

Ces trois commandes passent par `app_workdir.get_env_parameters()` / `set_env_parameters()`, jamais par `os.environ` direct.

---

### 2. Validation des vars requises avant `app::app/start`

Actuellement `app::app/start` vérifie seulement que `.wex/.env` existe. Il n'y a aucun check que les vars `required: true` des services installés sont présentes.

Résultat : le docker compose plante en cours de route avec une erreur cryptique.

**Objectif :** avant de lancer `app::config/build` + `docker compose up`, vérifier que toutes les vars marquées `required: true` dans les `service.yml` des services installés sont présentes dans `.wex/.env`.

**Comportement attendu :**
- Si des vars manquent : afficher un tableau (var / service / description) et proposer de les saisir interactivement (réutiliser la logique de `app::service/install` step 2)
- Si l'utilisateur refuse / annule : arrêt propre avec message explicite
- Si tout est OK : continuer normalement

**Implémentation :**
- Nouvelle méthode `app_workdir.get_missing_required_service_vars() -> dict[str, list[str]]` — itère les services installés (depuis `config.yml`), lit leurs `vars`, croise avec `.wex/.env`, retourne `{VAR_KEY: [service_name, description]}`
- Appelée dans `app__app__start()` après le check d'existence de `.wex/.env`

---

### 3. `core::env/configure` extensible par les addons

Actuellement `_CONFIGURABLE_KEYS` est hardcodé dans `configure.py` avec seulement `SSH_AUTH_SOCK`.

**Objectif :** les addons peuvent déclarer leurs propres vars machine-spécifiques via un hook.

**Approche :**
- Ajouter `get_local_configurable_keys() -> list[dict]` sur `AbstractAddonManager` (retourne `[]`)
- `core::env/configure` collecte les keys de tous les addons + les siennes propres
- Les clés suivent le même format que `_CONFIGURABLE_KEYS` : `{key, description, default_candidates}`

Cela permet par exemple à un futur addon de déclarer `DOCKER_HOST` ou un chemin local spécifique sans toucher au core.

---

### 4. `/var/www/[env]` — issue #10

La création du dossier `/var/www/[env]` lors du setup de l'environnement d'exécution de wex était prévue en 2023 (v5). Elle n'a pas été implémentée.

**Status :** pas de besoin concret exprimé depuis. À implémenter uniquement si un cas d'usage précis se présente.

**Action :** fermer l'issue GitLab #10 comme "non prioritaire / reprendre si besoin".

---

## Ordre de réalisation suggéré

1. Tâche 2 (validation avant start) — impact direct sur la fiabilité du workflow quotidien
2. Tâche 1 (`app::env/var/*`) — commodité CLI, évite les éditions manuelles de .env
3. Tâche 3 (configure extensible) — qualité d'architecture, faible urgence

La tâche 4 ne sera traitée que si un besoin réel se manifeste.
