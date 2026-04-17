# Erreurs subprocess — chaîne A → B → C

## Contexte

```
A (wex app::suite/publish)
  → shell_run(.wex/bin/app-manager app::package/commit-and-push)   # B
      → shell_run(git push -u origin ...)                           # C — root cause
```

Résultat actuel : B a déjà affiché son erreur. A re-affiche un `ShellCommandFailedException`
sur le subprocess B, ce qui duplique le message ou le noie.

## Ce qui est fait

- `ShellCommandFailedException` propagé depuis C jusqu'à A ✅
- `exec_argv()` affiche message propre + "To retry manually" ✅

## Ce qui reste

### Détecter qu'un subprocess est un wex

- [ ] Créer `shell_is_wex_subprocess(cmd) -> bool` dans `helpers/shell.py`
  — vérifie si `.wex/bin/app-manager` ou `bin/wex` est dans les args

### Silencer la re-affichage côté A

- [ ] Quand A reçoit une `ShellCommandFailedException` pour un subprocess wex détecté,
  afficher uniquement : `[SUB_PROCESS_FAILED] <commande> — see above.` sans répéter le détail
- [ ] Si le subprocess n'est pas wex (ex: git direct) → comportement actuel inchangé

## Sortie cible (A→B→C)

```
[SHELL_COMMAND_FAILED] Command exited with code 128
  Command : git push -u origin version-0.3.11
  Stderr  : error: src refspec version-0.3.11 does not match any

To retry manually:
  git push -u origin version-0.3.11
```

C'est l'erreur de C qui s'affiche. Les couches B et A ne répètent pas.
