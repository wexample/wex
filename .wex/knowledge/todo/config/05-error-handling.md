# Niveau transverse — Gestion d'erreurs robuste au boot

wex plante en stacktrace brute quand `APP_ENV` manque ou quand une env var requise
est absente au démarrage. Le mécanisme de gestion gracieuse existe déjà — il n'est
juste pas branché sur le boot.

---

## Contexte : ce qui existe déjà

`AppRuntimeException` (`packages/app/src/wexample_app/exception/app_runtime_exception.py`) :
- Sous-classe de `UndefinedException`
- Méthode `format_error_with_kernel()` : affiche un message propre, pas de stacktrace sauf `-vvv`
- Déjà utilisée par toutes les exceptions de commande (`CommandRunnerNotFoundException`, etc.)

Le handler dans `command_line_kernel.py:exec_argv()` :
```python
try:
    command_requests = self._build_command_requests_from_arguments(...)
except AppRuntimeException as e:
    e.format_error_with_kernel(kernel=self)   # message propre
    return
except Exception as e:
    self.io.error(exception=e, fatal=True)    # stacktrace brute
```

**Problème** : `setup()` est appelé **avant** `exec_argv()`, donc complètement hors du try/except.
Toute erreur levée pendant le boot (env manquante, config invalide) → stacktrace Python brute.

---

## Erreurs actuellement non couvertes

| Exception | Package | Étend | Résultat actuel |
|---|---|---|---|
| `MissingRequiredEnvVarError` | `helpers` | ??? | stacktrace brute |
| `KeyNotFoundError` | `helpers` | ??? | stacktrace brute |

Ces deux exceptions sont levées dans `HasEnvKeys._validate_env_keys()` et `get_env_parameter()`,
tous les deux appelés dans `setup()` — avant le handler.

---

## Tâches

### Option A — Faire hériter les erreurs d'env de `AppRuntimeException`

- [ ] Vérifier la hiérarchie actuelle de `MissingRequiredEnvVarError` et `KeyNotFoundError`
- [ ] Si elles étendent `UndefinedException` (même base que `AppRuntimeException`), les faire étendre `AppRuntimeException` directement
- [ ] **Problème** : `AppRuntimeException` est dans `wexample_app`, `MissingRequiredEnvVarError` est dans `wexample_helpers` — dépendance circulaire si helpers dépend de app
- [ ] Si dépendance circulaire : déplacer `AppRuntimeException` dans `wexample_helpers` ou créer une base commune dans helpers

### Option B — Wrapper le `setup()` dans le point d'entrée

- [ ] Dans le launcher bash ou le point d'entrée Python (`Kernel.__init__` ou équivalent), wrapper l'appel à `setup()` dans un try/except
- [ ] Catch `MissingRequiredEnvVarError` → afficher message clair + sortie propre (exit code 1)
- [ ] Catch `Exception` générique → afficher stacktrace avec hint `-vvv`
- [ ] Cette option ne résout pas le problème structurellement mais est la plus rapide à implémenter

### Option C (recommandée) — Base commune dans helpers

- [ ] Créer `wexample_helpers/exception/abstract_display_exception.py`
  - Méthode `get_user_message()` → message lisible
  - Méthode `get_error_code()` → code court type `MISSING_ENV_VAR`
- [ ] `MissingRequiredEnvVarError` et `KeyNotFoundError` étendent `AbstractDisplayException`
- [ ] `AppRuntimeException` étend aussi `AbstractDisplayException`
- [ ] Le handler de `exec_argv()` catch `AbstractDisplayException` (pas seulement `AppRuntimeException`)
- [ ] Un handler équivalent wrappant `setup()` fait pareil

### Aligner le message de `MissingRequiredEnvVarError`

- [ ] Le message actuel se contente de lister les clés manquantes
- [ ] Enrichir avec : description de la var (via `EnvVarSpec` — voir `02-env-var-system.md`), commande corrective, path du fichier où la setter
- [ ] Exemple de sortie cible :
  ```
  [MISSING_ENV_VAR] Required environment variable not set: APP_ENV
    Description: Application environment (local, staging, prod)
    Fix: Add APP_ENV=local to .env or .wex/local/env.yaml
  Run with -vvv for the full traceback.
  ```

---

## Fichiers concernés

| Fichier | Rôle |
|---|---|
| `packages/app/src/wexample_app/common/mixins/command_line_kernel.py:48` | `exec_argv()` — handler existant, à étendre ou compléter |
| `packages/app/src/wexample_app/exception/app_runtime_exception.py` | Base exception gracieuse |
| `packages/helpers/src/wexample_helpers/errors/missing_required_env_var_error.py` | À faire hériter de la bonne base |
| `packages/helpers/src/wexample_helpers/errors/key_not_found_error.py` | Idem |

---

## Ordre de priorité

1. **Court terme** : Option B — wrapper `setup()` pour stopper les plantages immédiats
2. **Moyen terme** : Option C — base commune pour une solution propre et extensible
3. **Long terme** : coupler avec `EnvVarSpec` (niveau 2) pour des messages enrichis
