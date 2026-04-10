# App-level filestate rules (ownership, service contributions)

## Problème concret déclencheur

Au démarrage de `store_mongo`, le répertoire `logs/` est créé par Docker avec `root:root`.
Le process mongo (uid 999) ne peut pas y écrire → crash exit 1.
Fix manuel : `sudo chown -R 999:999 logs/`.

Objectif : que ce fix soit **appliqué automatiquement** lors du `apply` filestate au démarrage, via une règle déclarative, sans intervention manuelle.

---

## Analyse de l'existant

### Ce qui existe déjà
- `app_addon_manager.create_app_workdir()` résout la classe workdir : cherche `.wex/app_workdir.py` → `AppWorkdir`, sinon `ManagedWorkdir`.
- `ManagedWorkdir.prepare_value()` injecte la structure filestate (`.wex/`, permissions globales 777, etc.).
- Les services contribuent au **runtime config** (docker-compose, env) via `get_runtime_contribution()` — mais **pas** à la structure filestate.
- Chaque app peut surcharger via `.wex/app_workdir.py`.

### Ce qui manque
1. **Pas d'option `owner` (uid:gid) dans filestate** — seul `mode.permissions` (octal) existe.
2. **Pas de mécanisme pour que les services déclarent leurs besoins filesystem** (ownership de répertoires, présence de fichiers avec perms spécifiques).
3. **Pas de merge YAML → filestate** depuis un fichier de config de l'app.

---

## Options envisagées

### A — `app_workdir.py` par app (existant, mais verbeux)
Surcharger `prepare_value()` dans `.wex/python/app_manager/app_workdir.py` de chaque app.
- ✅ Fonctionne maintenant, pattern déjà établi.
- ❌ Code Python par app pour quelque chose de déclaratif → lourd, non-reusable entre apps similaires.

### B — YAML app-level (`app_workdir.yml` ou section dans `config.yml`)
Lire un fichier YAML dans l'app qui décrit des règles filestate supplémentaires, mergées dans `prepare_value`.
- ✅ Déclaratif, accessible sans code Python.
- ❌ Duplique la config entre apps du même type (toutes les apps mongo auraient le même YAML).
- ❌ Pas de lien sémantique entre le service et ses besoins filesystem.

### C — Contribution filestate par service (recommandée)
Chaque service (mongo, postgres, redis…) peut déclarer une méthode `get_workdir_contribution()` qui retourne des règles filestate additionnelles. `ManagedWorkdir.prepare_value()` itère les services actifs et merge leurs contributions.
- ✅ Cohérent avec le pattern `get_runtime_contribution()` existant.
- ✅ Le service déclare lui-même ses besoins → DRY, reusable pour toutes les apps mongo.
- ✅ Peut cohabiter avec B (YAML) pour des overrides app-spécifiques.
- ❌ Nécessite d'ajouter l'option `owner` dans filestate (prérequis).

### D — `mongo_workdir.py` dans le package service
Classe workdir dédiée dans `wex-addon-services-db/services/mongo/workdir.py` qui étend `ManagedWorkdir` et override `prepare_value`. Wex la détecte et l'utilise quand mongo est le service principal.
- ✅ Encapsulation parfaite.
- ❌ Nécessite un mécanisme de résolution de classe workdir par service (à créer).
- ❌ Sur-ingénierie pour le cas présent ; la contribution (option C) est suffisante.

---

## Décision recommandée

**Approche C (contributions services) + prérequis `owner` dans filestate.**

L'option B (YAML app-level) peut être ajoutée en complément comme escape hatch pour des règles purement app-spécifiques, mais le cas mongo doit être résolu côté service.

---

## Roadmap d'implémentation

### Étape 1 — Ajouter `OwnerOption` dans filestate
**Package** : `wexample_filestate`
**Fichiers concernés** :
- `packages/filestate/src/wexample_filestate/option/mode_option.py` — ajouter `OwnerOption` dans `allowed_options`
- `packages/filestate/src/wexample_filestate/option/mode/owner_option.py` — créer l'option
- `packages/filestate/src/wexample_filestate/operation/` — créer `ChownOperation` (ou étendre l'opération de mode existante)

**Comportement attendu** :
```yaml
mode:
  owner: "999:999"   # ou "mongodb:mongodb"
  permissions: "750"
  recursive: true
```
- Supporte `"uid:gid"` (numérique) et `"user:group"` (symbolique).
- `build_operations()` détecte le owner actuel via `os.stat()` et génère un `ChownOperation` si différent.
- `ChownOperation.apply()` appelle `os.chown()` (ou `subprocess chown` pour les cas root → nécessite sudo ou un runner privilégié).

**Point à trancher** : pour chowner en 999:999 un dossier créé par root, il faut des droits root. Deux options :
- a) Utiliser `sudo chown` avec un wrapper (add sudoers rule au setup).
- b) Créer le dossier dès le départ avec le bon owner (empêche Docker de le créer root).
→ **Option b préférable** : si filestate crée `logs/` avant le premier `docker up`, Docker ne le recrée pas. `os.makedirs` + `os.chown` n'a pas besoin de sudo si le process wex tourne en tant que l'user courant et le dossier n'existe pas encore.

### Étape 2 — Mécanisme `get_workdir_contribution()` dans `AppService`
**Package** : `wexample_wex_addon_app`
**Fichiers concernés** :
- `wex-addon-app/src/wexample_wex_addon_app/service/app_service.py` — ajouter méthode `get_workdir_contribution() -> dict | None` (retourne `None` par défaut = pas de contribution)

**Signature** :
```python
def get_workdir_contribution(self) -> dict | None:
    """Return filestate children config to be merged into app workdir prepare_value."""
    return None
```

### Étape 3 — `ManagedWorkdir.prepare_value()` collecte les contributions
**Package** : `wexample_wex_addon_app`
**Fichier** : `wex-addon-app/src/wexample_wex_addon_app/workdir/managed_workdir.py`

Dans `prepare_value()`, après la définition de la structure `.wex/`, itérer les services actifs :
```python
for service in self.get_active_services():
    contribution = service.get_workdir_contribution()
    if contribution:
        raw_value["children"].extend(contribution.get("children", []))
```

`get_active_services()` existe probablement déjà (via runtime config) — vérifier le mixin `WithRuntimeConfigMixin`.

### Étape 4 — Implémenter `get_workdir_contribution()` dans le service mongo
**Package** : `wexample_wex_addon_services_db`
**Fichier** : `wex-addon-services-db/src/wexample_wex_addon_services_db/services/mongo/app_service.py` (à créer ou étendre)

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

### Étape 5 — (Optionnel) YAML app-level override
**Mécanisme** : si `.wex/app_workdir.yml` existe, `ManagedWorkdir.prepare_value()` le lit et merge son contenu `children` après les contributions services.

Utile pour des besoins purement app-spécifiques (ex : un dossier custom propre à une instance).

### Étape 6 — Générer le mongo-keyfile si vide
Le fichier `mongo-keyfile` doit contenir une clé non-vide. Deux options :
- a) Traiter ça dans filestate via une `ContentOption` (contenu généré si vide).
- b) Ajouter une étape de setup dans la commande `app start` / `service mongo setup`.

**Recommandation** : option b, car générer une clé cryptographique n'est pas du ressort de filestate. Créer une commande `mongo::setup` (ou hook `service/mongo/setup`) qui :
1. Génère la clé si `mongo-keyfile` est vide : `openssl rand -base64 756`
2. Set les permissions et owner

Ce setup doit tourner **avant** le premier `docker up` et être idempotent.

---

## Ordre d'implémentation suggéré

| # | Tâche | Package | Priorité |
|---|-------|---------|----------|
| 1 | `OwnerOption` dans filestate + `ChownOperation` | `wexample_filestate` | Bloquant |
| 2 | `get_workdir_contribution()` dans `AppService` | `wexample_wex_addon_app` | Bloquant |
| 3 | Collect contributions dans `ManagedWorkdir.prepare_value()` | `wexample_wex_addon_app` | Bloquant |
| 4 | Contribution mongo (`logs/`, `mongo-keyfile` owner+perms) | `wexample_wex_addon_services_db` | Bloquant |
| 5 | Commande/hook `mongo::setup` pour keyfile | `wexample_wex_addon_services_db` | Nécessaire |
| 6 | YAML app-level override (`app_workdir.yml`) | `wexample_wex_addon_app` | Nice-to-have |

---

## Points à trancher avant d'implémenter

1. **Sudo pour chown** : on suppose que filestate crée les dossiers *avant* Docker (pas de chown root nécessaire). À confirmer : est-ce qu'on peut garantir que le premier `app start` tourne avant le premier `docker up` ?

2. **Résolution des services actifs dans workdir** : comment `ManagedWorkdir` connaît-il les services actifs au moment du `prepare_value` ? Via `self.get_config()["services"]` ? Vérifier que le runtime config est disponible à ce stade.

3. **Format du `owner`** : string `"uid:gid"` numérique uniquement (simple) ou aussi symbolique `"user:group"` (requiert résolution `/etc/passwd` ou dans-container) ? Recommandation : numérique uniquement en v1.
