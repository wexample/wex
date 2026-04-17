# Niveau transverse — Fondation exception : base commune dans helpers

Prérequis structural pour tous les autres chantiers d'erreurs (06, boot, env).

Le problème central : `AppRuntimeException` (qui donne des messages propres) vit dans
`wexample_app`, mais les exceptions levées dans `wexample_helpers` (`MissingRequiredEnvVarError`,
`KeyNotFoundError`, et à venir `ShellCommandFailedException`) ne peuvent pas en hériter
sans créer une dépendance circulaire `helpers → app`.

---

## Tâches

### Créer `AbstractDisplayException` dans helpers

- [ ] Créer `packages/helpers/src/wexample_helpers/exception/abstract_display_exception.py`
  ```python
  class AbstractDisplayException(Exception):
      error_code: str = "UNKNOWN_ERROR"
      message: str
      data: dict | None = None

      def get_user_message(self) -> str: ...
      def get_error_code(self) -> str: ...
  ```
- [ ] `AppRuntimeException` étend `AbstractDisplayException` (au lieu de `UndefinedException` directement)
- [ ] `MissingRequiredEnvVarError` étend `AbstractDisplayException`
- [ ] `KeyNotFoundError` étend `AbstractDisplayException`
- [ ] `ShellCommandFailedException` (voir `error-handling-ux.md`) étend `AbstractDisplayException`

### Brancher le handler sur `AbstractDisplayException`

- [ ] `exec_argv()` dans `command_line_kernel.py:48` : catch `AbstractDisplayException` en plus de `AppRuntimeException`
- [ ] `command_request.execute()` dans `command_request.py:124` : idem
- [ ] Wrapper `setup()` dans le point d'entrée du kernel pour les erreurs au boot :
  ```python
  try:
      kernel.setup()
  except AbstractDisplayException as e:
      print(f"[{e.get_error_code()}] {e.get_user_message()}")
      sys.exit(1)
  ```

### Enrichir `MissingRequiredEnvVarError`

- [ ] Message actuel : liste brute des clés manquantes
- [ ] Cible (couplé à `EnvVarSpec` de `env-var-system.md`) :
  ```
  [MISSING_ENV_VAR] Required environment variable not set: APP_ENV
    Description: Application environment (local, staging, prod)
    Fix: Add APP_ENV=local to .env or .wex/local/env.yaml
  ```

---

## Fichiers concernés

| Fichier | Action |
|---|---|
| `packages/helpers/src/wexample_helpers/exception/abstract_display_exception.py` | Nouveau — base commune |
| `packages/helpers/src/wexample_helpers/errors/missing_required_env_var_error.py` | Étendre `AbstractDisplayException` |
| `packages/helpers/src/wexample_helpers/errors/key_not_found_error.py` | Étendre `AbstractDisplayException` |
| `packages/app/src/wexample_app/exception/app_runtime_exception.py` | Étendre `AbstractDisplayException` |
| `packages/app/src/wexample_app/common/mixins/command_line_kernel.py:48` | Handler étendu |
| `packages/app/src/wexample_app/common/command_request.py:124` | Handler étendu |

---

## Dépendances

- Bloque partiellement `error-handling-ux.md` (`ShellCommandFailedException` a besoin de cette base)
- Bloque partiellement `env-var-system.md` (enrichissement du message `MissingRequiredEnvVarError`)
