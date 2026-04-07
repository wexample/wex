# config/write — Roadmap v6

## Vision

`config/write` est un **orchestrateur pur**. Il ne connaît pas les services.
Il demande à chaque service "qu'est-ce que tu contribues ?" et merge.

Pipeline final :
```
1. _runtime   → runtime.yml         (une seule écriture, toutes contributions mergées)
2. _env       → docker.env          (projection mécanique du runtime.yml, pas de logique métier)
3. _docker    → docker-compose.runtime.yml
```

`AppService.get_runtime_contribution()` est le contrat unique entre un service et config/write.

---

## Étapes

### ✅ STEP 0 — Squelette vide
`config/write` s'exécute sans erreur, imprime "OK".
> Validé.

---

### STEP 1 — `_runtime` : base app config
**Ce qu'on fait :**
- Écrire `runtime.yml` depuis `build_runtime_config_value()` + extras de base :
  `{ env, name, host.ip, started: false }`
- Pas de services encore.

**Résultat :** `runtime.yml` écrit, config/write passe.

---

### STEP 2 — `AppService.get_runtime_contribution()` + merge dans `_runtime`
**Ce qu'on fait :**
- Ajouter `get_runtime_contribution(app_env: str) -> dict` sur `AppService`
- Implémentation par défaut : passthrough de `config.yml service.{name}` (host, port, name, password, user...)
- `_runtime` itère sur les services, merge toutes les contributions dans runtime.yml

**Contrat :**
```python
# AppService.get_runtime_contribution() retourne, ex pour mysql :
{
    "service": {
        "mysql": { "host": "network_mysql", "port": 3306, "name": "network", ... }
    }
}
```

**Résultat :** runtime.yml contient les données de chaque service. config/write passe.

---

### STEP 3 — `service.yml` : contributions déclaratives
**Ce qu'on fait :**
- `service.yml` peut déclarer des contributions calculées au runtime :
```yaml
runtime:
  bind:
    web_php_ini: php/web.{env}.ini   # résolu relatif à .wex/
```
- `AppService.get_runtime_contribution()` lit ce bloc et résout les chemins

**Résultat :** `bind.web_php_ini` dans runtime.yml via symfony/service.yml, sans Python.
config/write passe.

---

### STEP 4 — `_env` : projection mécanique du runtime.yml
**Ce qu'on fait :**
- `_env` lit `runtime.yml` et projette mécaniquement → `docker.env`
- Table de mapping v5→v6 centralisée :
  ```
  name             → RUNTIME_NAME (v5) + APP_PROJECT (v6)
  path.app         → RUNTIME_PATH_APP (v5) + APP_PATH (v6)
  path.setup       → RUNTIME_PATH_APP_ENV (v5) + APP_SETUP_PATH (v6)
  bind.*           → RUNTIME_BIND_* (v5) + BIND_* (v6)
  service.*.compose → RUNTIME_SERVICE_*_YML_ENV (v5) + SERVICE_*_COMPOSE (v6)
  service.*.*      → SERVICE_*_* (v5+v6)
  ```
- Zéro logique service-spécifique dans `_env`

**Résultat :** docker.env complet. config/write passe.

---

### STEP 5 — `_docker` : docker-compose.runtime.yml
**Ce qu'on fait :**
- Injecter les compose files déclarés dans `service.*.compose` du runtime.yml
- Injecter le compose de base de l'app (`.wex/docker/docker-compose.yml`)
- `docker compose config` → `docker-compose.runtime.yml`

**Résultat :** docker-compose.runtime.yml généré. `app::app/start` peut utiliser le fichier.

---

## Ce qu'on ne fait PAS dans config/write

- Écriture de fichiers de config service (mysql.cnf, etc.) → `@mysql::config/runtime`
- Gestion des domaines/proxy → étape ultérieure
- Gestion user/group/uid/gid → étape ultérieure
- Templates de fichiers de config service → étape ultérieure

---

## Fichiers concernés

| Fichier | Rôle |
|---|---|
| `wex-addon-app/.../commands/config/write.py` | Orchestrateur |
| `wex-addon-app/.../service/app_service.py` | `get_runtime_contribution()` |
| `wex-addon-*/services/*/service.yml` | Contributions déclaratives |
| `wex-addon-*/services/*/docker/docker-compose.yml` | Compose par service |
