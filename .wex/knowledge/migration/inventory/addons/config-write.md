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

### ✅ STEP 1 — `_runtime` : base app config
**Ce qu'on fait :**
- Écrire `runtime.yml` depuis un dict vide + extras de base : `{ env, name, host.ip, started: false }`
- `name` lu depuis `get_project_name()` → `get_config().search("global.name")` (corrigé : ne lit plus le runtime)
- Pas de services encore.

**Résultat :** `runtime.yml` propre, zéro bruit v5.
> Validé.

---

### ✅ STEP 2 — `AppService.get_runtime_contribution()` + merge dans `_runtime`
**Ce qu'on fait :**
- `get_runtime_contribution() -> dict` sur `AppService`
- Lit `config.yml service.{name}` (host, port, name, password, user...) + path compose
- `_runtime` itère sur les services, merge toutes les contributions

**Contrat :**
```python
# AppService.get_runtime_contribution() retourne, ex pour mysql :
{
    "service": {
        "mysql": { "host": "network_mysql", "port": 3306, "compose": "/path/to/docker-compose.yml", ... }
    }
}
```

**Résultat :** runtime.yml contient uniquement les données v6, une seule écriture.
> Validé.

---

### ✅ STEP 3 — `service.yml` : contributions déclaratives (bind avec résolution en couches)

**Structure de fichiers dans l'app :**
```
.wex/
  php/
    web.ini          # base, commité, toujours présent
  env/
    local/
      php/
        web.ini      # override local (commité aussi — seul .env est exclu du git)
    prod/
      php/
        web.ini      # override prod
```

**Déclaration dans `service.yml` :**
```yaml
runtime:
  bind:
    web_php_ini: php/web.ini   # chemin stable, résolution env transparente
```

**Résolution dans `AppService.get_runtime_contribution()` :**
1. Cherche `.wex/env/{env}/php/web.ini`
2. Fallback sur `.wex/php/web.ini`
3. Erreur explicite si aucun n'existe (pas de masquage silencieux)

**Résultat :** `bind.web_php_ini` dans runtime.yml pointe sur le fichier le plus spécifique disponible.
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
