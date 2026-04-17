# Niveau 1 — Health check au démarrage

Vérifier que l'environnement est correctement configuré pour git/SSH
lors du boot du kernel, d'un `wex health`, **et à l'installation de wex**.

---

## Objectif

L'utilisateur reçoit un feedback immédiat et clair si SSH n'est pas disponible,
**avant** d'exécuter une commande qui en aurait besoin.
Pas de "Permission denied (publickey)" au fond d'une stacktrace.

---

## Tâches

### Créer un mixin `HasSshCheck`

- [ ] Créer `packages/helpers-git/src/wexample_helpers_git/common/mixin/has_ssh_check.py`
- [ ] Méthode `check_ssh_auth()` → retourne un `SshCheckResult` (ok, agent_missing, no_key_loaded)
- [ ] Méthode `get_ssh_check_required()` → `bool` (défaut `False`, surchargeable par sous-classe)
- [ ] Méthode `assert_ssh_available()` → lève `SshAuthNotAvailableError` si check échoue

### Implémenter les vérifications

- [ ] Vérifier que `SSH_AUTH_SOCK` est défini et pointe vers un socket existant (`os path.exists`)
- [ ] Vérifier qu'au moins une clé est chargée dans l'agent (`ssh-add -l` exit code 0)
- [ ] Fournir un message d'erreur actionnable avec la commande corrective (`eval $(ssh-agent); ssh-add`)

### Intégrer dans le kernel

- [ ] Créer `wex/wex-core/src/wexample_wex_core/common/mixin/has_kernel_ssh_check.py`
- [ ] Le mixin surcharge `get_ssh_check_required()` selon la config locale (voir niveau 2)
- [ ] Appel dans `Kernel.setup()` après `_init_env_file()` et avant `_init_workdir()`
- [ ] Ne pas mettre la logique SSH dans `abstract_kernel.py` (trop bas niveau)

### Commande `wex health`

- [ ] Créer la commande `health` dans `wex-core` (elle n'existe pas encore)
- [ ] Ajouter un check SSH dans le rapport de santé
- [ ] Format de sortie : `[OK]` / `[WARN]` / `[FAIL]` avec message explicatif

### Health check à l'installation

- [ ] Identifier le point d'entrée de l'installation de wex (APT post-install hook ou script dédié)
- [ ] Appeler le health check SSH à la fin de l'installation
- [ ] Afficher un résumé lisible : ce qui est OK, ce qui manque, comment corriger
- [ ] L'installation ne doit pas échouer si SSH n'est pas configuré (warn, pas fail) — l'utilisateur peut configurer SSH après

---

## Fichiers concernés

| Fichier | Rôle |
|---|---|
| `packages/app/src/wexample_app/common/abstract_kernel.py:71` | `setup()` — point d'entrée boot |
| `wex/wex-core/src/wexample_wex_core/common/kernel.py` | Kernel wex — où intégrer le check |
| `packages/helpers-git/src/wexample_helpers_git/helpers/git.py:362` | `_git_resolve_ssh_env()` — logique SSH actuelle à refactorer |

---

## Contraintes

- Ne pas mettre de détails GNOME/keyring dans `abstract_kernel.py`
- Le mixin `HasSshCheck` doit rester dans `helpers-git`, pas dans `helpers` (pas de dépendance SSH dans le package générique)
- Le health check doit être non-bloquant par défaut (warn, pas crash) sauf si `get_ssh_check_required()` retourne `True`
