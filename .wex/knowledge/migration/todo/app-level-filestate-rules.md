# App-level filestate rules (ownership, service contributions)

## Problème déclencheur

Au démarrage de `store_mongo`, le répertoire `logs/` est créé par Docker avec `root:root`.
Le process mongo (uid 999) ne peut pas y écrire → crash exit 1.
Objectif : ce fix appliqué automatiquement lors du `apply` filestate au démarrage.

---

## Architecture de résolution (décisions prises)

### Accès aux services dans `prepare_value()`

`ManagedWorkdir` a `self.parent_io_handler` qui est le kernel.
`AppAddonManager.from_kernel(self.parent_io_handler)` retourne le manager.
`.get_app_services(self)` retourne la liste des `AppService` actifs (lu depuis `config.yml` sur disque).
Le `config.yml` est disponible sur disque au moment de `prepare_value()` — pas de circular dependency.

### Sudo

`app/start` lance docker avec `as_sudo`. Le `ChownOperation` utilisera donc `subprocess(['sudo', 'chown', ...])`.
Le cas sans sudo (dossier créé par wex avant docker) n'est pas garanti, donc sudo est la seule voie fiable.

### Trois mécanismes qui coexistent (par priorité croissante)

```
[1] Service contribution     ← déclaré dans le package service (ex: wex-addon-services-db)
[2] config.yml app-level     ← section `workdir.children` dans .wex/config.yml de l'app
[3] app_workdir.py           ← override Python complet pour cas complexes
```

Ordre de merge dans `prepare_value()` : contributions services → config.yml → stop.
`app_workdir.py` override `prepare_value()` entièrement (pattern existant, il gagne toujours).

---

## Étape 1 — `OwnerOption` + `ChownOperation` dans filestate

**Package** : `wexample_filestate`

### Syntaxe YAML (définitive)

```yaml
mode:
  owner: "999:999"          # uid:gid numérique
  owner: "mongodb:mongodb"  # user:group symbolique (résolu via pwd.getpwnam / grp.getgrnam)
  owner: "999"              # uid seul, gid inchangé
  permissions: "750"        # octal string ou int
  recursive: true
```

Les deux formats (numérique et symbolique) sont supportés dès v1.
Résolution symbolique : `pwd.getpwnam(user).pw_uid` + `grp.getgrnam(group).gr_gid` — stdlib Python, pas de dépendance externe.

### Fichiers à créer / modifier

| Fichier | Action |
|---|---|
| `option/mode/owner_option.py` | Nouveau. Valide et normalise le format (`str` → `tuple[int, int]`). Accepte `"uid:gid"`, `"user:group"`, `"uid"`. |
| `option/mode_option.py` | Ajouter `OwnerOption` dans `allowed_options`. |
| `operation/chown_operation.py` | Nouveau. `build()` : compare `os.stat().st_uid/st_gid` à la cible. `apply()` : `subprocess(['sudo', 'chown', '-R'?, 'uid:gid', path])`. Respecte `recursive`. |
| `item/abstract_item_target.py` | `build_operations()` doit appeler `ChownOperation.build()` si `owner` défini dans `mode`. |

### Comportement

- `build_operations()` génère un `ChownOperation` seulement si le owner courant diffère de la cible.
- `recursive=true` → flag `-R` sur le chown.
- `permissions` et `owner` sont indépendants, peuvent être utilisés séparément.

---

## Étape 2 — `get_workdir_contribution()` dans `AppService`

**Package** : `wexample_wex_addon_app`  
**Fichier** : `service/app_service.py`

```python
def get_workdir_contribution(self) -> dict | None:
    """Filestate children rules injected into the app workdir at prepare_value time."""
    return None
```

Retourne `None` par défaut. Les services qui ont des besoins filesystem l'override.

---

## Étape 3 — Collecte dans `ManagedWorkdir.prepare_value()`

**Fichier** : `workdir/managed_workdir.py`

À la fin de `prepare_value()`, après la structure `.wex/` :

```python
# 1. Service contributions
from wexample_wex_addon_app.app_addon_manager import AppAddonManager
manager = AppAddonManager.from_kernel(self.parent_io_handler)
for service in manager.get_app_services(self):
    contribution = service.get_workdir_contribution()
    if contribution:
        raw_value.setdefault("children", []).extend(
            contribution.get("children", [])
        )

# 2. config.yml app-level (section workdir.children)
app_config = self.get_config()
workdir_extra = app_config.search("workdir.children") if app_config else None
if workdir_extra:
    raw_value.setdefault("children", []).extend(workdir_extra.to_list())
```

---

## Étape 4 — Contribution du service mongo

**Package** : `wexample_wex_addon_services_db`  
**Fichier** : `services/mongo/app_service.py` (créer ou étendre la classe existante)

```python
def get_workdir_contribution(self) -> dict:
    return {
        "children": [
            {
                "name": "logs",
                "type": DiskItemType.DIRECTORY,
                "should_exist": True,
                "mode": {
                    "owner": "999:999",
                    "permissions": "750",
                    "recursive": True,
                },
            },
            {
                "name": "mongo-keyfile",
                "type": DiskItemType.FILE,
                "should_exist": True,
                "mode": {
                    "owner": "999:999",
                    "permissions": "400",
                },
            },
        ]
    }
```

---

## Étape 5 — Génération du mongo-keyfile

Filestate vérifie l'existence et les permissions du fichier, mais **pas son contenu**.
La génération de la clé est du ressort d'une commande setup, pas de filestate.

**Solution** : hook ou commande `mongo::service__setup` (idempotente) qui tourne avant `docker up` :

```python
# Si mongo-keyfile est vide (taille 0), générer la clé
keyfile_path = self.get_path() / "mongo-keyfile"
if keyfile_path.stat().st_size == 0:
    key = subprocess.check_output(['openssl', 'rand', '-base64', '756'])
    key = key.replace(b'\n', b'')
    keyfile_path.write_bytes(key)
```

Filestate s'occupe ensuite du chown/chmod via la contribution mongo (étape 4).

---

## Syntaxe YAML app-level (section `workdir` dans `.wex/config.yml`)

Pour des règles spécifiques à une instance, sans créer d'`app_workdir.py` :

```yaml
# .wex/config.yml
service:
  mongo: {}

workdir:
  children:
    - name: custom-data
      type: directory
      should_exist: true
      mode:
        owner: "1000:1000"
        permissions: "755"
```

---

## Ordre d'implémentation

| # | Tâche | Package | Statut |
|---|-------|---------|--------|
| 1 | `OwnerOption` + `ChownOperation` dans filestate | `wexample_filestate` | TODO |
| 2 | `get_workdir_contribution()` dans `AppService` | `wexample_wex_addon_app` | TODO |
| 3 | Collecte contributions + config.yml dans `ManagedWorkdir` | `wexample_wex_addon_app` | TODO |
| 4 | Contribution mongo (`logs/`, `mongo-keyfile`) | `wexample_wex_addon_services_db` | TODO |
| 5 | Commande `mongo::service__setup` pour keyfile | `wexample_wex_addon_services_db` | TODO |
