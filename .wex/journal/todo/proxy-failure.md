# Ticket : Proxy prod failure — wex 6.0.56 / helpers 6.7.0

## Résumé

Le proxy nginx (`wex-proxy`) en prod a échoué à démarrer après une tentative d'installation du service via `wex app::service/install -s proxy --force`. Cela a mis hors ligne l'ensemble des sites proxifiés (16 domaines). Résolu manuellement en restaurant un backup.

## Environnement

- Serveur : wexample.com (SSH: `weeger@wexample.com`, clé `~/.ssh/id_rsa`)
- Chemin app proxy : `/var/www/prod/wex-proxy`
- Wex installé : `/usr/lib/wex/`
- **Version wex en prod : 6.0.56**
- **Version `wexample-helpers` en prod : 6.7.0**
- Version `wexample-helpers` locale (attendue) : **6.8.0**

## Chronologie du problème

1. `wex app::app/start` sur `/var/www/prod/hat` échoue avec "no service selected"
2. Le fichier `.wex/docker/docker-compose.yml` est absent de `wex-proxy` — le service proxy n'a jamais été installé correctement
3. Tentative de `wex app::service/install -s proxy --force` → crash :

```
ImportError: cannot import name 'file_copytree_merge_yaml'
from 'wexample_helpers.helpers.file'
(/usr/lib/wex/.venv/lib/python3.12/site-packages/wexample_helpers/helpers/file.py)
```

4. La fonction `file_copytree_merge_yaml` a été ajoutée dans `wexample-helpers` **6.8.0** et dans `wexample-wex-addon-app` lors d'une session de dev récente
5. La prod tourne toujours sur **6.7.0** — le package n'a pas été publié
6. Cercle vicieux : proxy en rade → pas de GitLab → pas de CI/CD → pas d'apt → impossible de mettre à jour wex
7. Résolution d'urgence : copie manuelle des samples depuis le venv (`/usr/lib/wex/.venv/.../services/proxy/samples/`) vers `/var/www/prod/wex-proxy/` via SSH, puis `app::app/start`
8. Le proxy a démarré mais a cassé les autres sites (mauvaise config). Rollback vers backup par l'utilisateur.

## Cause racine

Le package `wexample-helpers` 6.8.0 (et les dépendances `wexample-wex-addon-app` associées) **n'ont jamais été publiés sur le dépôt apt** hébergé sur le serveur lui-même. Ce problème aurait dû être résolu avant de modifier `service/install.py` pour importer `file_copytree_merge_yaml`.

## Ce qu'il faut faire

1. **Publier `wexample-helpers` >= 6.8.0** sur le dépôt apt du serveur
2. **Publier `wexample-wex-addon-app`** dans sa version incluant `file_copytree_merge_yaml` dans `commands/service/install.py`
3. **Mettre à jour wex sur le serveur** (`apt upgrade wex` ou équivalent) pour passer de 6.0.56 à la version courante
4. **Vérifier** que `wex app::service/install -s proxy --force` fonctionne sur le serveur après mise à jour
5. **Investiguer** pourquoi le démarrage manuel du proxy a cassé les autres sites (config réseau Docker ?)

## Rappel architectural

Le dépôt apt est hébergé sur le serveur lui-même — toute panne du proxy coupe le CI/CD et donc la capacité de publier des correctifs. Il faut un plan de continuité pour ce cas (procédure de mise à jour manuelle documentée).
