

## Contexte : wex — problème SSH dans les subprocesses git

### Le problème immédiat

wex est un outil CLI Python (installé via APT ou en local) qui orchestre des
commandes git à travers une stack Python :

bin/wex (bash) → Python kernel → asyncio subprocesses → git

Quand wex est lancé depuis un terminal qui n'a pas SSH_AUTH_SOCK dans son env
(typiquement : terminal VSCode, sudo, ou tout process sans session GNOME),
tous les appels git qui nécessitent une auth SSH échouent silencieusement avec
"Permission denied (publickey)" après 3 retries.

Fix temporaire déjà en place (à revoir) :
packages/helpers-git/src/wexample_helpers_git/helpers/git.py
→ fonction `_git_resolve_ssh_env()` qui tente d'auto-détecter
/run/user/{uid}/keyring/ssh si SSH_AUTH_SOCK est absent.

Ce fix est fragile : GNOME-centrique, couvre seulement `git_run()`, ne couvre
pas les `shell_run(["git", ...])` directs, mauvaise abstraction.

---

### Fichiers clés à lire en priorité

**Kernel / setup :**
packages/app/src/wexample_app/common/abstract_kernel.py
→ setup() ligne 71, get_expected_env_keys() ligne 66
packages/app/src/wexample_app/common/mixins/  (mixins du kernel)

**Git helpers :**
packages/helpers-git/src/wexample_helpers_git/helpers/git.py
→ git_run(), _git_resolve_ssh_env(), git_ensure_upstream(),
git_push_follow_tags(), git_set_upstream()
packages/helpers/src/wexample_helpers/helpers/shell.py
→ shell_run() — le runner asyncio sous-jacent, gère env=None/dict

**App workdir (appelle git dans les publish flows) :**
wex/wex-addon-app/src/wexample_wex_addon_app/workdir/code_base_workdir.py
→ commit_changes(), push_to_deployment_remote(), push_changes()

**Gestion d'env / config locale :**
.wex/local/ — configs locales par machine (pattern existant à explorer)
packages/app/src/wexample_app/common/abstract_kernel.py → _init_env_file()

**Launcher :**
wex/local/wex/bin/wex — point d'entrée bash, source .env, lance Python
wex/local/wex/.wex/bin/app-manager — lance Python pour les sous-apps

---

### La mission, à plusieurs niveaux

**Niveau 1 — Health check au démarrage**
Lors de l'install initiale ou d'un `wex health` / self-check, vérifier que
l'environnement est correctement configuré pour que les commandes git
fonctionnent (SSH_AUTH_SOCK présent et socket accessible, clé chargée, etc.).
Endroit probable : abstract_kernel.setup() ou un mixin dédié.

**Niveau 2 — Système de gestion des variables d'env**
Créer un système qui permette d'administrer les variables d'env nécessaires
(SSH_AUTH_SOCK, APP_ENV, etc.) de façon structurée, avec déclaration explicite
des variables requises par feature/addon, et intégré ou aligné avec le système
de config locale .wex/local/ déjà existant.
L'idée : chaque addon/feature déclare ses env vars requises, le kernel les
valide au boot et peut guider l'utilisateur pour les setter.

**Niveau 3 — Auth SSH unifiée et confortable**
Exiger les variables nécessaires avant tout appel git qui nécessite SSH.
Si SSH_AUTH_SOCK manque : soit on détecte proprement le socket agent (avec une
liste de candidats cross-platform, pas juste GNOME), soit on demande le mot de
passe une fois via TTY et on le passe à tous les appels de la session, bref un
système unifié qui ne bloque pas silencieusement. L'utilisateur doit avoir un
feedback clair et une résolution guidée, pas un "Permission denied" au fond
d'une stacktrace.

**Niveau 4 — Audit de tous les appels git**
Passer en revue l'ensemble des appels git dans le codebase (helpers-git,
wex-addon-app, toute la suite) pour s'assurer que :
- tous passent par git_run() (et non shell_run(["git", ...]) en direct)
- git_run() applique le bon env SSH
    - les retries et les messages d'erreur sont cohérents
    - le fix temporaire _git_resolve_ssh_env() est soit formalisé proprement
      soit supprimé au profit du niveau 2/3

                                    ---

### Ce qu'on NE veut PAS
- Un fix GNOME-only hardcodé dans une lib générique (helpers-git)
- Du SSH_AUTH_SOCK auto-magique qui marche parfois et échoue silencieusement
- Des appels git directs via shell_run bypassing git_run() (uniformité des outils)
- Umplémenter ça dans abstract_kernel, qui connaîtrait les détails de gnome-keyring, ce n'est pas sa place

### Démarche suggérée
Commence par lire les fichiers listés, cartographie tous les appels git et
tous les endroits où des env vars sont déclarées/validées, puis propose un
plan d'implémentation niveau par niveau avant de coder quoi que ce soit.

Faire plusieurs fichiers de roadmap contenant des cases à cocher a placer dans un sous dossier todo/config/*
faire plusieurs fichiers plutot qu'un seul.