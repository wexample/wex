# Roadmap : app commands YAML + app-manager

> Deux catégories : **migrations** (appliquées automatiquement sur tous les repos d'apps)
> et **changements de code** (modification unique dans un seul repo).

---

## Changements de code

### C1 — Simplifier `resources/app-manager.sh` (wex-addon-app)

Réduire le script à l'essentiel — plus de task ID, plus de pip install, plus de `__main__.py` :

```bash
#!/usr/bin/env bash
set -euo pipefail

CONFIG_FILE="/etc/wex.conf"
if [[ -f "$CONFIG_FILE" ]]; then source "$CONFIG_FILE"; fi

if [[ -z "${CORE_BIN:-}" ]]; then
    CORE_BIN="$(which wex 2>/dev/null || true)"
fi

if [[ -z "${CORE_BIN:-}" ]]; then
    echo "Error: Unable to locate 'wex'."
    exit 1
fi

exec "$CORE_BIN" "$@"
```

---

### C2 — Supprimer `AppManagerKernel` (wex-core)

`AppManagerKernel` existait uniquement pour skipper le `REQUEST_ID` en `argv[1]`.
Ce concept est mort. Supprimer la classe et tous ses imports.

---

### ~~C3~~ → fusionné dans M2 (`migration_wex_6_0_16`)

La règle est la même partout : tous les `.wex/` ont le même rôle. La migration 6.0.16 couvre
indistinctement les repos addon et les apps utilisateur.

---

### C4 — Features YAML manquantes (wex-core)

#### Y1 — `title:` sur les steps (trivial)
`CoreYamlCommandRunner._execute_step` affiche `step.get("title")` avant exécution.
Ajouter `"title"` à `AbstractScriptRunner.get_step_options()`.

#### Y2 — Bare string steps (trivial)
Dans `_make_executor`, si un step est `str`, convertir en `{runner: bash, script: valeur}`.

#### Y3 — Runner `exec` générique
```yaml
- runner: exec
  interpreter: [node, -e]
  script: console.log("hello")
```
Nouveau `ExecScriptRunner` dans `yaml/runners/`. Enregistré dans `ScriptRunnerRegistry`.

#### Y4 — `sync: false` par step (faible priorité)
`BashScriptRunner` : `subprocess.Popen` sans `.wait()` si `sync: false`.

#### Y5 — `app_should_run:` (après validation app-commands)
Guard sur les steps : vérifie que les containers tournent. Dépend de `app::app/started`.

#### Y6 — `webhook:` dans le YAML (wex-core)
`YamlCommandDefinition._parse_decorators` : reconnaître `{name: webhook}`, poser `_wex_webhook = True`.

#### Y7 — `pass_previous:` sur attach (complexe, plus tard)
Output du step précédent passé en argument à la commande attachée.

---

## Migrations (appliquées automatiquement sur toutes les apps)

### M1 — Fix `migration_wex_6_0_0` → réécrire `.wex/bin/app-manager`

**Problème :** La migration crée un symlink vers un chemin hardcodé machine-specific qui n'existe plus.

**Fix :** Remplacer le contenu de `apply()` par un simple appel à `managed_workdir.apply()` (ou écrire directement le contenu de `resources/app-manager.sh`). Le filestate de `managed_workdir.prepare_value()` déploie déjà le bon script.

La migration doit aussi supprimer le symlink cassé si présent avant de réécrire.

---

### M2 — Nettoyage `app_manager` (✅ `migration_wex_6_0_16`)

**Cible :** Tout repo ayant un `.wex/python/app_manager/` (apps utilisateur **et** repos addon wex)

**Actions :**
1. Supprimer `__main__.py` si présent
2. Supprimer `pyproject.toml` si présent
3. Supprimer `requirements.txt` si présent
4. Supprimer `.wex/python/app_manager/` si vide après nettoyage

`app_workdir.py` est **préservé** s'il existe.

---

### M3 — Renommer `.wex/command/` → `.wex/commands/` + réécriture YAML v5→v6 (✅ `migration_wex_6_0_17`)

**Cible :** Toutes les apps ayant encore un `.wex/command/`

**Actions :**
1. Renommer le dossier
2. Réécrire chaque fichier YAML selon le mapping :

| Clé v5 | Action v6 |
|--------|-----------|
| `type:` | Supprimer |
| `help:` | → `description:` |
| `command:` (decorator block) | Supprimer |
| `properties: [as_sudo]` | → `decorators: [{name: sudo}]` |
| `properties: [app_webhook]` | → `decorators: [{name: webhook}]` |
| `properties: [{name: alias, ...}]` | → `decorators: [{name: alias, args: ...}]` |
| `properties: [{name: attach, ...}]` | → `decorators: [{name: attach, args: ...}]` |
| Step bare string `- echo "foo"` | → `{runner: bash, script: "echo foo"}` |
| Step `context: container` + `container_name: x` | → `{runner: docker, service: x}` |
| Step `interpreter: [python3, -c]` + `script:` | → `{runner: python, script:}` |
| Step `interpreter: [python3]` + `file:` | → `{runner: python, file:}` |
| Step `type: bash-file` + `file:` | → `{runner: bash, file:}` |
| Step `title:` | Garder |
| Step `variable:` | Garder |
| Step `sync: true` | Supprimer |
| Step `sync: false` | → `# TODO: async not yet supported` |
| Step `app_should_run:` | → `# TODO: not yet supported` |

---

## Ordre d'exécution

| Priorité | Item | Type | Repo | Effort |
|----------|------|------|------|--------|
| 1 | C1 — Simplifier `app-manager.sh` | Code | wex-addon-app | Trivial |
| 2 | C2 — Supprimer `AppManagerKernel` | Code | wex-core | Petit |
| 3 | ~~C3~~ → M2 — Nettoyage `app_manager` (tous repos) | ✅ Migration 6.0.16 | wex-addon-app | — |
| 4 | M1 — Fix migration 6.0.0 | Migration | wex-addon-app | Petit |
| 5 | ~~M2~~ fusionné dans 6.0.16 | — | — | — |
| 6 | C4/Y1 — `title:` sur les steps | Code | wex-core | Trivial |
| 7 | C4/Y2 — Bare string steps | Code | wex-core | Trivial |
| 8 | ~~M3~~ — `command` → `commands` + YAML rewriting | ✅ Migration 6.0.17 | wex-addon-app | — |
| 9 | C4/Y6 — `webhook:` dans le YAML | Code | wex-core | Petit |
| 10 | C4/Y3 — Runner `exec` générique | Code | wex-core | Moyen |
| 11 | C4/Y4 — `sync: false` | Code | wex-core | Petit |
| 12 | C4/Y5 — `app_should_run:` | Code | wex-core + addon-app | Après app-commands |
| 13 | C4/Y7 — `pass_previous:` | Code | wex-core | Complexe |
