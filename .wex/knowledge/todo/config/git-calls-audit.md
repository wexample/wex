# Niveau 4 — Audit et uniformisation de tous les appels git

Passer tous les appels git en direct via `shell_run(["git", ...])` vers `git_run()`,
et vérifier la cohérence des retries/erreurs.

---

## Contexte

Audit complet effectué. Résultat :

### Appels via `git_run()` (conformes)
- `git.py:274-332` — `git_push_follow_tags()` et variantes push/tag ✅
- `code_base_workdir.py:150-155` — wrapper `git_run()` dans la workdir ✅
- `flutter_pubspec_yaml_file.py:21-28` — `git remote get-url` ✅

### Appels directs `shell_run(["git", ...])` (à migrer)

| Fichier | Ligne | Commande | SSH requis ? | Priorité |
|---|---|---|---|---|
| `packages/helpers/src/wexample_helpers/helpers/repo.py` | 18 | `git rev-parse HEAD` | Non | Basse |
| `packages/helpers/src/wexample_helpers/helpers/repo.py` | 21 | `git diff` | Non | Basse |
| `packages/helpers-git/.../helpers/git.py` | 35 | `git add -A` | Non | Moyenne |
| `packages/helpers-git/.../helpers/git.py` | 36-40 | `git commit -m` | Non | Moyenne |
| `wex/wex-addon-app/.../workdir/code_base_workdir.py` | 206-217 | `git merge` | Non | Moyenne |
| `wex/wex-addon-app/.../workdir/code_base_workdir.py` | 225-236 | `git merge` | Non | Moyenne |

> Note : aucun de ces appels directs ne nécessite SSH (ce sont des opérations locales).
> La migration vers `git_run()` est néanmoins requise pour l'uniformité,
> la cohérence des retries, et pour couvrir d'éventuels futurs besoins.

---

## Tâches

### Migration de `repo.py`

- [x] Déplacé `packages/helpers/.../helpers/repo.py` → `packages/helpers-git/.../helpers/repo.py`
  - Migré `shell_run(["git", ...])` → `git_run([...])` pour les deux appels
  - Aucun consommateur existant, suppression directe sans shim

### Migration des appels dans `git.py`

- [x] `packages/helpers-git/.../helpers/git.py:35`
  - `git_commit_all_with_message()` : remplacer `shell_run(["git", "add", "-A"], ...)` par `git_run(["add", "-A"], ...)`
- [x] `packages/helpers-git/.../helpers/git.py:36-40`
  - Remplacer `shell_run(["git", "commit", "-m", message], ...)` par `git_run(["commit", "-m", message], ...)`

### Migration des appels dans `code_base_workdir.py`

- [x] `wex/wex-addon-app/.../workdir/code_base_workdir.py` — deux `git merge` dans `merge_to_main()` → `self.git_run(["merge", ...])`

### Vérifier la cohérence des retries et messages d'erreur

- [ ] `git_run()` dans `git.py:388-397` — vérifier que les retries sont cohérents avec `shell_run()`
- [ ] S'assurer que les erreurs git (exit code non-zero) lèvent une exception typée, pas un crash silencieux
- [ ] Créer `GitCommandError` dans `helpers-git/exception/` si elle n'existe pas

### Supprimer `_git_resolve_ssh_env()` (après niveau 3)

- [ ] Une fois `SshAgentResolver` en place (niveau 3), supprimer `_git_resolve_ssh_env()` de `git.py:362-386`
- [ ] Retirer l'appel à `_git_resolve_ssh_env()` dans `git_run()` et remplacer par `SshAgentResolver`
- [ ] Vérifier qu'aucune autre fonction n'appelle `_git_resolve_ssh_env()` directement

### Recherche exhaustive pour s'assurer qu'il ne reste aucun appel direct

- [ ] Grep `shell_run.*"git"` dans tout le codebase → liste complète
- [ ] Grep `subprocess.*git` pour détecter des appels encore plus bas niveau
- [ ] Vérifier `os.system("git` et `Popen.*git` (peu probable mais à confirmer)

---

## Fichiers concernés

| Fichier | Lignes | Action |
|---|---|---|
| `packages/helpers/src/wexample_helpers/helpers/repo.py` | 18, 21 | Migrer vers `git_run()` ou déplacer dans helpers-git |
| `packages/helpers-git/.../helpers/git.py` | 35-40 | Migrer `git_commit_all_with_message()` |
| `packages/helpers-git/.../helpers/git.py` | 362-386 | Supprimer `_git_resolve_ssh_env()` (après niveau 3) |
| `wex/wex-addon-app/.../workdir/code_base_workdir.py` | 206-217, 225-236 | Migrer `merge_to_main()` |

---

## Contraintes

- Ne pas casser les commandes git locales (add, commit, diff) en leur injectant inutilement une logique SSH
- L'uniformité vers `git_run()` est l'objectif, mais `git_run()` doit rester léger pour les commandes locales (voir niveau 3 — distinction SSH vs local)
- Migrer `repo.py` en dernier : vérifier d'abord la compatibilité des dépendances entre packages
