# Niveau transverse — UX des erreurs : du crash brut au message actionnable

wex a déjà un bon mécanisme (`AppRuntimeException.format_error_with_kernel()`) pour
les erreurs "connues". L'objectif est d'étendre ce traitement à tous les cas courants :
subprocess, chaîne A→B→C, Ctrl+C, et d'ajouter un fichier de crash report.

---

## État actuel (mis à jour)

`exec_argv()` gère maintenant : `KeyboardInterrupt` ✅, `AppRuntimeException` ✅, `ShellCommandFailedException` ✅, `Exception` → crash report ✅.

Reste : chaîne A→B→C (Cas 2).

---

## Cas 1 — Wrapping de `CalledProcessError`

### Problème

`shell_run()` re-raise la `CalledProcessError` brute. Elle n'hérite pas de `AppRuntimeException`,
donc le handler général ne la traite pas proprement.

### Solution : `ShellCommandFailedException`

- [x] Créer `packages/helpers/src/wexample_helpers/exception/shell_command_failed_exception.py`
  > Hérite de `UndefinedException` (helpers ne dépend pas de app). Stocke cmd, returncode, stderr, stdout.

- [x] Dans `shell_run()`, `shell_run_async()`, `shell_stream_async()` : wrap `CalledProcessError` → `ShellCommandFailedException`
- [x] Handler dans `exec_argv()` et `command_request.execute()` : affiche message propre + "To retry manually"

### Format de sortie souhaité

```
[SHELL_COMMAND_FAILED] Command exited with code 128
  Command : git push -u origin version-0.3.11
  Stderr  : error: src refspec version-0.3.11 does not match any

To retry manually:
  git push -u origin version-0.3.11
```

- [x] Afficher la commande en version copy-pasteable (`shlex.join(cmd)` si list)
- [x] Afficher stderr si disponible et non vide
- [x] Bloc "To retry manually" avec la commande formatée

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
{app_workdir}/tmp/logs/errors/YYYY-MM-DD_HH-MM-SS_<command>.log
```
→ `_get_crash_report_dir()` dans `command_line_kernel.py` (default générique via `workdir/tmp/logs/errors`), déclaré dans `KernelWorkdir.prepare_value()`.

### Implémentation

- [x] Créer `packages/app/src/wexample_app/helpers/crash_report.py`
  - `write_crash_report(exception, kernel) -> Path`
  - Écrit : timestamp, commande exécutée, traceback complet, env (filtré des secrets)
- [x] Dans le `except Exception` de `exec_argv()` : appel `write_crash_report` + message avec le chemin
- [x] Rotation des logs : garder les 50 derniers fichiers, supprimer les plus vieux
- [x] Ne pas logger `SSH_AUTH_SOCK`, `*_PASSWORD`, `*_TOKEN`, `*_SECRET` dans l'env dump
- [x] `logs/errors/` ajouté dans `KernelWorkdir.prepare_value()` → `tmp/logs/errors/`
- [x] `_get_crash_report_dir()` : default `~/.wex/logs/errors/`, override wex-core → `workdir/tmp/logs/errors/`

### Message terminal

```
[UNEXPECTED_ERROR] An unexpected error occurred.
  Full crash report: ~/.wex/logs/errors/2026-04-17_14-32-01_app-suite-publish.log
Run with -vvv to see the traceback directly in the terminal.
```

---

## Reste à faire

- Cas 2 — Chaîne A→B→C (le plus complexe, dépend des précédents)
