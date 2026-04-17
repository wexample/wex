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

### Commande `default::check/health`

La convention de nommage wex est `addon__group__command` → invoqué `addon::group/command`.
Le groupe `check` existe déjà dans `wex-core/addons/default/commands/check/` (voir `check/hi.py`).
La commande health s'y place naturellement : `default__check__health` → `default::check/health`.

- [x] Créer `wex/wex-core/src/wexample_wex_core/addons/default/commands/check/health.py`
- [x] Format de sortie : `[OK]` / `[WARN]` / `[FAIL]` par item avec message explicatif
- [x] Env vars : s'appuyer sur `HasEnvKeys.get_expected_env_keys()` et `_get_missing_env_keys()` (déjà disponibles via la hiérarchie du kernel)
- [x] SSH : warning actionnable via `SshAgentResolver` (voir `ssh-auth-unified.md`)
- [ ] Optionnel : intégrer filestate en dry run pour détecter ce que filestate corrigerait sans modifier les fichiers — `FileStateDryRunResult._apply_single_operation()` retourne `True` sans écrire, c'est déjà le bon mécanisme. À affiner selon l'utilité réelle dans un health check.

### Health check à l'installation

- [ ] Identifier le point d'entrée de l'installation de wex (APT post-install hook ou script dédié)
- [ ] Appeler `default::check/health` à la fin de l'installation (ou une version allégée)
- [ ] Afficher un résumé lisible : ce qui est OK, ce qui manque, comment corriger
- [ ] L'installation ne doit pas échouer si SSH n'est pas configuré (warn, pas fail)

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
