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

### Extraire et refactorer en `SshAgentResolver`

- [ ] Créer `packages/helpers-git/src/wexample_helpers_git/service/ssh_agent_resolver.py`
- [ ] Classe `SshAgentResolver` avec méthode `resolve() -> str | None`
  - Retourne le path du socket valide trouvé, ou `None`
- [ ] Liste de candidats cross-platform dans l'ordre de priorité :
  ```python
  SOCKET_CANDIDATES = [
      # Linux — GNOME Keyring
      "/run/user/{uid}/keyring/ssh",
      # Linux — GnuPG Agent
      "/run/user/{uid}/gnupg/S.gpg-agent.ssh",
      # Linux — XDG fallback
      "{XDG_RUNTIME_DIR}/keyring/ssh",
      # Linux — systemd user session
      "/run/user/{uid}/ssh-agent.socket",
      # macOS — Keychain / launchd
      "/private/tmp/com.apple.launchd.*/Listeners",  # glob
      # Generic — SSH_AUTH_SOCK from env (priorité 1, vérif socket)
      # Agent standard démarré manuellement
      "{HOME}/.ssh/agent.sock",
      "{TMPDIR}/ssh-*/agent.*",  # glob
  ]
  ```
- [ ] Vérifier que le fichier existe ET est un socket Unix valide (`stat.S_ISSOCK`)
- [ ] Support des patterns glob pour macOS / agents dynamiques

### Stratégie de fallback quand aucun agent n'est trouvé

- [ ] Option 1 — Warning non-bloquant avec instruction corrective :
  ```
  [WARN] SSH agent not found. Git push/pull via SSH may fail.
  Fix: eval $(ssh-agent) && ssh-add ~/.ssh/id_rsa
  Or set SSH_AUTH_SOCK in .wex/local/env.yaml
  ```
- [ ] Option 2 — Prompt TTY interactif si la commande est interactive :
  - Demander le chemin du socket ou lancer `ssh-agent` automatiquement
  - Stocker le résultat pour la durée de la session (singleton)
- [ ] Option 3 — Lever `SshAgentNotFoundError` si `get_ssh_check_required()` est `True`
- [ ] Configurer le comportement via `.wex/local/env.yaml` : `SSH_FAIL_STRATEGY: warn|prompt|fail`

### Intégrer `SshAgentResolver` dans `git_run()`

- [ ] Remplacer l'appel à `_git_resolve_ssh_env()` par `SshAgentResolver().resolve()`
- [ ] Supprimer `_git_resolve_ssh_env()` une fois la migration validée
- [ ] `git_run()` ne doit pas crasher si le resolver retourne `None` pour des commandes locales (add, commit, diff)

### Distinguer commandes git SSH vs locales

- [ ] Créer `GIT_SSH_COMMANDS = {"push", "pull", "fetch", "clone", "ls-remote"}`
- [ ] `git_run()` n'appelle `SshAgentResolver` que si la commande est dans `GIT_SSH_COMMANDS`
- [ ] Cela évite un warning SSH lors d'un simple `git status` ou `git log`

### Session-level caching

- [ ] `SshAgentResolver` est un singleton de session (résout une fois, réutilise)
- [ ] Invalider le cache si `SSH_AUTH_SOCK` change dans l'env entre deux appels

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
