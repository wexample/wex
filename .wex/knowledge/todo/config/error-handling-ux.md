# Niveau transverse — UX des erreurs : du crash brut au message actionnable

wex a déjà un bon mécanisme (`AppRuntimeException.format_error_with_kernel()`) pour
les erreurs "connues". L'objectif est d'étendre ce traitement à tous les cas courants :
subprocess, chaîne A→B→C, Ctrl+C, et d'ajouter un fichier de crash report.

---

## État actuel

### Ce qui marche déjà

`exec_argv()` dans `command_line_kernel.py:48` :
```python
try:
    command_requests = self._build_command_requests_from_arguments(...)
except AppRuntimeException as e:
    e.format_error_with_kernel(kernel=self)   # message propre, no traceback
    return
except Exception as e:
    self.io.error(exception=e, fatal=True)    # traceback brut
    return
```

`CommandTypeNotFoundException`, `CommandRunnerNotFoundException`, etc. → tous propres.

### Ce qui plante en brut

- `CalledProcessError` levée par `shell.py:115` → tombe dans `except Exception` → stacktrace Python complète
- `KeyboardInterrupt` (Ctrl+C) → pas catchée → stacktrace Python complète
- Subprocess chain A→B→C → double (ou triple) trace, racine enfouie en bas

---

## Cas 1 — Wrapping de `CalledProcessError`

### Problème

`shell_run()` re-raise la `CalledProcessError` brute. Elle n'hérite pas de `AppRuntimeException`,
donc le handler général ne la traite pas proprement.

### Solution : `ShellCommandFailedException`

- [ ] Créer `packages/helpers/src/wexample_helpers/exception/shell_command_failed_exception.py`
  ```python
  class ShellCommandFailedException(Exception):
      cmd: list[str] | str
      returncode: int
      stderr: str | None
      stdout: str | None
  ```
  > Note : ne peut pas hériter de `AppRuntimeException` (helpers ne dépend pas de app).
  > Voir `error-handling.md` pour la base commune à créer.

- [ ] Dans `shell_run()` au `except subprocess.CalledProcessError`, wrap en `ShellCommandFailedException` avant de re-raise
- [ ] `AppRuntimeException` handler dans `exec_argv()` / `command_request.execute()` doit aussi catcher `ShellCommandFailedException`

### Format de sortie souhaité

```
[SHELL_COMMAND_FAILED] Command exited with code 128
  Command : git push -u origin version-0.3.11
  Stderr  : error: src refspec version-0.3.11 does not match any

To retry manually:
  git push -u origin version-0.3.11
```

- [ ] Afficher la commande en version copy-pasteable (`shlex.join(cmd)` si list)
- [ ] Afficher stderr si disponible et non vide
- [ ] Bloc "To retry manually" avec la commande formatée

---

## Cas 2 — Chaîne de subprocess A → B → C

### Problème

```
A (wex app::suite/publish)
  → shell_run(.wex/bin/app-manager app::package/commit-and-push)   # B
      → shell_run(git push -u origin ...)                           # C — root cause
```

Résultat actuel : 3 tracebacks, la vraie erreur (git push) est en bas, noyée.

### Détection d'un subprocess wex

Un subprocess wex a un pattern reconnaissable dans ses args :
- Contient `.wex/bin/app-manager`
- Contient `--output-format json` ou `--output-target file`

Quand un subprocess wex échoue, **il a déjà affiché son propre message d'erreur**.
A ne devrait donc pas ré-afficher l'erreur de B.

### Solution : propagation structurée via JSON

- [ ] Quand B plante, son output JSON contient déjà l'erreur (ou devrait la contenir)
- [ ] Créer un flag dans la réponse JSON : `"error": {"code": "...", "message": "...", "cmd": [...]}`
- [ ] Quand A reçoit une `ShellCommandFailedException` pour un subprocess wex, parser le JSON stderr/stdout de B
- [ ] Si B a déjà propagé une erreur structurée → A affiche uniquement : `[SUB_PROCESS_FAILED] app::package/commit-and-push failed — see above.` sans répéter le détail
- [ ] Si B n'a pas propagé d'erreur structurée (B a crashé en brut) → A affiche le stderr de B tel quel

### Heuristique de détection

- [ ] Créer `shell_is_wex_subprocess(cmd) -> bool` dans `helpers/shell.py`
  - Vérifie si `.wex/bin/app-manager` ou `bin/wex` est dans les args

### Format de sortie souhaité (A→B→C)

```
[SHELL_COMMAND_FAILED] Command exited with code 128
  Command : git push -u origin version-0.3.11
  Stderr  : error: src refspec version-0.3.11 does not match any

To retry manually:
  git push -u origin version-0.3.11
```
→ C'est l'erreur de C qui s'affiche, pas B, pas A. Les couches intermédiaires sont supprimées.

---

## Cas 3 — KeyboardInterrupt (Ctrl+C)

### Problème

Ctrl+C → Python affiche une stacktrace + `KeyboardInterrupt`. C'est inutile et perturbant.

### Solution

- [x] `except KeyboardInterrupt` dans `exec_argv()` → `self.io.log("\nInterrupted.")` + `sys.exit(130)`
- [x] `sys.exit(130)` → exit code standard pour signal INT, compatible avec les scripts shell parent
- [x] La boucle `execute_kernel_command_and_print()` est désormais dans le même try/except

---

## Cas 4 — Fichier de crash report

### Objectif

Pour les exceptions non gérées (vraiment inattendues), écrire la stacktrace complète dans un fichier
plutôt que de la déverser sur le terminal.

### Emplacement

```
~/.wex/logs/errors/YYYY-MM-DD_HH-MM-SS_<command>.log
```
ou, si on préfère par projet :
```
{project}/.wex/tmp/logs/error/YYYY-MM-DD_HH-MM-SS.log
```
→ Préférer `~/.wex/logs/` (global, toujours accessible même si le projet n'est pas init)

### Implémentation

- [ ] Créer `wex/wex-core/src/wexample_wex_core/helpers/crash_report.py`
  - `write_crash_report(exception, kernel) -> Path`
  - Écrit : timestamp, commande exécutée, traceback complet, env (filtré des secrets)
- [ ] Dans le `except Exception` de `exec_argv()` :
  ```python
  except Exception as e:
      path = write_crash_report(exception=e, kernel=self)
      self.io.error(message=f"Unexpected error. Full report: {path}")
      sys.exit(1)
  ```
- [ ] Rotation des logs : garder les 50 derniers fichiers, supprimer les plus vieux
- [ ] Ne pas logger `SSH_AUTH_SOCK`, `*_PASSWORD`, `*_TOKEN`, `*_SECRET` dans l'env dump

### Message terminal

```
[UNEXPECTED_ERROR] An unexpected error occurred.
  Full crash report: ~/.wex/logs/errors/2026-04-17_14-32-01_app-suite-publish.log
Run with -vvv to see the traceback directly in the terminal.
```

---

## Récapitulatif des fichiers à créer / modifier

| Fichier | Action |
|---|---|
| `packages/helpers/src/wexample_helpers/exception/shell_command_failed_exception.py` | Nouveau — wrapper de `CalledProcessError` |
| `packages/helpers/src/wexample_helpers/helpers/shell.py:115` | Wrap `CalledProcessError` → `ShellCommandFailedException` |
| `packages/app/src/wexample_app/common/mixins/command_line_kernel.py:48` | Catcher `ShellCommandFailedException` + `KeyboardInterrupt` |
| `packages/app/src/wexample_app/common/command_request.py:124` | Idem dans `execute()` |
| `wex/wex-core/src/wexample_wex_core/helpers/crash_report.py` | Nouveau — écriture fichier de crash |

---

## Ordre d'implémentation suggéré

1. `KeyboardInterrupt` → 5 lignes, gain immédiat, risque zéro
2. `ShellCommandFailedException` → élimine 80% des stacktraces visibles
3. Crash report file → confort pour le debug des cas restants
4. Chaîne A→B→C → le plus complexe, dépend des deux précédents
