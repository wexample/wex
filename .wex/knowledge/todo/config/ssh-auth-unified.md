# Niveau 3 — Auth SSH unifiée et cross-platform

Remplacer `_git_resolve_ssh_env()` (GNOME-centrique, dans helpers-git) par
un système unifié, cross-platform, avec feedback clair et résolution guidée.

---

## Contexte actuel

`_git_resolve_ssh_env()` dans `git.py:362-386` :
- Vérifie 3 candidats hardcodés (GNOME Keyring, GnuPG Agent, XDG_RUNTIME_DIR)
- Silencieuse si aucun socket trouvé → retourne `None` → git échoue quand même
- Couvre seulement les appels via `git_run()`, pas les `shell_run(["git", ...])` directs
- Mal placée : logique d'infra SSH dans une lib utilitaire git

---

## Tâches

## ✅ Fait

### `SshAgentResolver`

- [x] Créé `packages/helpers-git/src/wexample_helpers_git/service/ssh_agent_resolver.py`
- [x] `resolve() -> str | None` — retourne le path du socket valide ou `None`
- [x] Candidats cross-platform : GNOME Keyring, GnuPG Agent, XDG, systemd, macOS launchd, `~/.ssh/agent.sock`, `TMPDIR/ssh-*/agent.*`
- [x] Vérification `stat.S_ISSOCK` — socket Unix valide
- [x] Support des patterns glob pour macOS / agents dynamiques
- [x] `SSH_AUTH_SOCK` depuis l'env — priorité 1
- [x] Session-level caching + `invalidate_cache()`

### Solution retenue (simplifiée)

- [x] `_git_resolve_ssh_env()` supprimé, `SshAgentResolver` supprimé (YAGNI)
- [x] `git_run()` simplifié : juste `shell_run(["git"] + cmd)`, pas de logique SSH
- [x] `_init_env_file_yaml()` injecte maintenant dans `os.environ` — les subprocesses héritent
- [x] `Kernel._init_local_env()` charge `.wex/local/env.yml` dans `os.environ` + `env_config`
- [x] `default::check/health` vérifie `SSH_AUTH_SOCK` directement dans `os.environ`

## ✅ Complet

---

## Fichiers concernés

| Fichier | Action |
|---|---|
| `packages/helpers-git/src/wexample_helpers_git/helpers/git.py:362-386` | Supprimer `_git_resolve_ssh_env()`, utiliser `SshAgentResolver` |
| `packages/helpers-git/src/wexample_helpers_git/service/ssh_agent_resolver.py` | Nouveau — résolution cross-platform |
| `packages/helpers-git/src/wexample_helpers_git/exception/ssh_agent_not_found_error.py` | Nouveau — exception typée |

---

## Contraintes

- Pas de dépendance à `gnome-keyring` ou `libsecret` — uniquement filesystem + socket check
- `SshAgentResolver` ne doit pas importer du code wex-core (pas de dépendance vers le haut)
- Le resolver doit fonctionner sans kernel (utilisable en standalone depuis helpers-git)
- Compatibilité macOS (si jamais le tool est porté)
