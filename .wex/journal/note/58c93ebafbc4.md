# Technique pour récupérer la version wex (complète todo e8153ff7ac95)

Written: 2026-08-27
Author: agent:main

Complète le todo `e8153ff7ac95` (Migration config.yml : ajouter clé wex.version manquante).

Pour lire la version wex courante depuis du code exécuté dans un workdir, la bonne technique est `context.kernel.workdir.get_setup_version()` — c'est ce que fait déjà `core__version__get` dans `wex-core/src/wexample_wex_core/addons/core/commands/version/get.py`.

À ne pas confondre avec la technique de lecture directe de `version.txt` via `context.kernel.entrypoint_path.parent`, qui a été proposée puis écartée en cours de discussion — elle lit la version du package installé, pas celle du workdir courant.

`app/init` (`init.py`) a été corrigé dans cette conversation pour utiliser `get_setup_version()` et écrire la clé `wex.version` dans `config.yml`. Le fix de l'init est fait ; il reste la migration pour les configs déjà créées sans cette clé, objet du todo `e8153ff7ac95`.
