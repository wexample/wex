# Bug: régression helper/proxy entre v5 et v6

## Constat

Le flux `app/start` v6 a perdu plusieurs comportements utiles du système de helpers v5.

En v5:
- `app/start` détecte si l'app a besoin d'un helper
- si besoin, il crée le helper via `helper/start`
- le helper est ensuite démarré comme une app normale
- l'app principale démarre ensuite
- le mécanisme est générique côté helper, même si le cas courant est le proxy
- `helper/stop` existe aussi

En v6:
- `helper/start` crée le proxy "à la main" en écrivant directement des fichiers
- `app/init` n'est pas utilisé pour créer le helper
- la notion de helper est devenue implicite et en pratique limitée au seul proxy
- `helper/stop` a disparu
- `app/start` du proxy affiche des informations incohérentes

## Symptômes observés

Quand le proxy démarre en v6:
- message `App "wex-proxy" started in local environment`
- URL proposée: `http://wex-proxy.wex`
- suggestions:
  - `app::db/go`
  - `app::app/go`
  - `app::app/stop`

Ces sorties sont incorrectes:
- le proxy n'a pas de domaine applicatif propre à exposer
- le proxy n'a pas de service DB, donc `app::db/go` n'a pas de sens

## Écart fonctionnel v5 → v6

### 1. Création du helper

v5:
- `helper/start` crée l'app helper via `app/init`
- la structure de l'app helper reste une vraie app Wex, construite par le flux standard

v6:
- `helper/start` supprime/recrée `/var/www/{env}/wex-proxy`
- écrit `config.yml`, `.env`, `docker-compose.yml`, `wex.conf` manuellement

Conséquence:
- logique plus fragile
- duplication de comportement normalement porté par `app/init`
- risque de divergence entre app helper et app standard

### 2. Généralité du mécanisme helper

v5:
- `helper/start` / `helper/stop` sont pensés comme commandes de helper génériques

v6:
- le code est proxy-centric
- `app/start` contient une logique spéciale "proxy helper" en dur
- aucune base claire pour d'autres helpers

### 3. Extinction du helper

v5:
- `helper/stop` existe

v6:
- commande absente

Conséquence:
- asymétrie start/stop
- régression fonctionnelle

### 4. UX de fin de démarrage

v5:
- l'affichage final dépend du contexte réel de l'app
- pas de suggestion DB si l'app n'a pas de DB

v6:
- `_complete` dans `app/start` propose toujours `app::db/go`
- affiche les domaines si `app.domains` existe, même pour le proxy

Conséquence:
- sortie confuse pour les helpers

## Cause probable

La migration v6 a simplifié un mécanisme sophistiqué en visant uniquement le cas proxy minimal:
- helper créé from scratch
- absence de `app/init`
- absence de `helper/stop`
- logique de fin de `app/start` non contextualisée selon les services réellement présents

## Attendu minimal pour correction

- réintroduire un vrai flux helper au lieu d'une création "freestyle"
- éviter que `helper/start` réécrive brutalement le proxy s'il existe déjà
- restaurer `helper/stop`
- rendre la logique helper à nouveau générique, même si seul le proxy est supporté dans un premier temps
- corriger `_complete` dans `app/start`:
  - pas de domaine affiché pour le proxy tant qu'il n'a pas de domaine propre déclaré
  - pas de suggestion `app::db/go` sans service DB principal

## Fichiers à revoir

- v5:
  - `/home/weeger/Desktop/WIP/WEB/WEXAMPLE/WEX/local/wex-5/addons/app/command/app/start.py`
  - `/home/weeger/Desktop/WIP/WEB/WEXAMPLE/WEX/local/wex-5/addons/app/command/helper/start.py`
  - `/home/weeger/Desktop/WIP/WEB/WEXAMPLE/WEX/local/wex-5/addons/app/command/helper/stop.py`
- v6:
  - `/home/weeger/Desktop/WIP/WEB/WEXAMPLE/PACKAGES/PYTHON/wex/wex-addon-app/src/wexample_wex_addon_app/commands/app/start.py`
  - `/home/weeger/Desktop/WIP/WEB/WEXAMPLE/PACKAGES/PYTHON/wex/wex-addon-app/src/wexample_wex_addon_app/commands/helper/start.py`
  - `/home/weeger/Desktop/WIP/WEB/WEXAMPLE/PACKAGES/PYTHON/wex/wex-addon-app/src/wexample_wex_addon_app/commands/helper/`

## Notes

- `app/init` n'est pas migré à ce stade, donc une vraie restauration du flux v5 demandera soit sa migration, soit une abstraction équivalente dédiée aux helpers
- pour un correctif court terme, on peut déjà corriger l'UX de `app/start` sans attendre la refonte complète des helpers
