# Refonte de l'architecture master

## Contexte

Le master actuel (mai 2026) est fonctionnel mais a plusieurs frictions structurelles qui se sont accumulées au fil des sessions :

- `project.yml > stacks > apps` liste des **paths d'apps** (`${LOCAL}/tpa`, `${LOCAL}/oscar`…). Si une app est renommée, déplacée ou supprimée, le fichier YAML pète. Vu cette session : oscar viré, mais la stack tpa référençait encore `${LOCAL}/oscar` jusqu'à correction manuelle.
- `master.local.yml > MASTER_APP_PATHS` mélange la *définition des dossiers à scanner* et la *liste explicite des apps*. Comportement implicite.
- Pas de registre des hosts : les IPs sont éclatées dans N fichiers `.wex/env/<env>/config.yml` d'apps. Friction relevée chantier #8 de `master.md`.
- Pas de registre des apps non plus : chaque appel `master::info/show` re-scanne le disque, refait la découverte. Pas de mémoire entre runs.
- Apparition / disparition d'une app traitée silencieusement par le scan — pas d'alerte si une app disparaît du disque.

L'idée est de refondre le master sur des principes plus solides, en gardant la rétro-compat le temps de la transition.

## Principes cibles

### 1. Apps autodescriptives

Une app = un dossier qui contient un `.wex/config.yml` avec :
```yaml
global:
  name: tpa           # identité de l'app, indépendante du dossier
  version: 3.5.82
  ...
```

Le **nom** dans la config est l'identifiant canonique. Le **dossier** est un détail d'organisation (peut bouger sans casser les références).

### 2. Stacks par nom ou tag, pas par path

Aujourd'hui :
```yaml
stacks:
  tpa:
    apps:
      - ${LOCAL}/tpa
      - ${LOCAL}/oscar       # ← path en dur, fragile
```

Cible :
```yaml
stacks:
  tpa:
    apps: [tpa, oscar]       # ← noms canoniques
    # OU
    tags: [tpa-core]         # ← des apps déclarent `tags: [tpa-core]` dans leur config
```

Une app peut porter plusieurs tags (`tags: [tpa-core, web, php]`). Une stack peut combiner liste explicite + filtres par tag.

### 3. Découverte centralisée

Aujourd'hui `apps:` au top de `project.yml` mélange discovery et déclaration. À séparer :

- **`master.local.yml`** définit où chercher les apps (varie par machine — local vs serveur, etc.) :
  ```yaml
  app_discovery_paths:
    - ${LOCAL}/*
    - ${PACKAGES}/*
    - ${PROJECT}/*/*
  ```
- **`project.yml`** ne déclare plus la liste — il décrit la structure logique (stacks, DNS, etc.) — c'est versionné et identique entre machines.

### 4. Auto-enrollement & registres

Master maintient deux registres :

#### Registre des apps (`apps.yml`, versionné)

Mis à jour à chaque scan. Format type :
```yaml
apps:
  tpa:
    name: tpa
    path_hint: local/tpa             # indicatif, pour rappel
    version: 3.5.82
    tags: [tpa-core, web]
    enrolled_at: 2026-05-28
  plausible:
    name: plausible
    path_hint: local/plausible
    version: 1.0.0
    tags: [analytics]
    enrolled_at: 2026-05-28
```

#### Registre des hosts/remotes (`hosts.yml`, versionné en partie, secrets en local)

```yaml
hosts:
  tpa_prod:
    ip: 51.210.104.199
    type: ovh-vps
    discovered_via: tpa/.wex/env/prod/config.yml
  tpa_dev:
    ip: 152.228.175.159
    discovered_via: tpa/.wex/env/dev/config.yml
  wexample_prod:
    ip: 151.80.23.108
  syrtis_prod:
    ip: 79.137.89.25
```

À noter : les `remotes[].host` dans les configs d'apps sont des **sources de vérité primaires**. Le registre maître ne fait que les agréger.

#### Comportement d'enrollment

- `wex master::scan` (ou `master::enroll`) parcourt les discovery paths
- Lit chaque `.wex/config.yml` trouvé
- Pour chaque nouvelle app : ajoute au `apps.yml` versionné + ajoute le path éventuellement à un cache local non-versionné (`apps.cache.yml`)
- Pour chaque nouvelle remote vue dans les `.wex/env/*/config.yml` : ajoute à `hosts.yml`
- **Disparition** : si une app/host disparaît du disque, **ne pas supprimer du registre automatiquement** — émettre un warning (`WARNING: app 'oscar' was enrolled but no longer found in discovery paths; run 'master::registry/clear oscar' to remove`)

Le registre est résistant aux glitches — un dossier rmd par erreur ne supprime pas la mémoire.

### 5. Référencement croisé

Avec les registres en place :

- Une app peut référencer un host par nom : `remotes[].host: ${HOST_TPA_PROD}` (debloque #6.5 et #9 de [master.md](master.md))
- Une stack peut composer des apps par tag ou nom
- Master commands prennent des noms (`wex master::host/spawn --based-on tpa_prod`) plutôt que des paths

## Workflow d'ajout d'une nouvelle app

Aujourd'hui (mai 2026) :
1. Créer le dossier `local/myapp/`
2. Initialiser `.wex/config.yml`
3. Éditer `project.yml` pour ajouter le path à `apps:` (souvent oublié — le `${MASTER_APP_PATHS}` glob s'en occupe heureusement)
4. Si déploiement : créer `.wex/env/prod/config.yml` avec `remotes[].host: <ip>` (IP en dur)
5. Refaire pour chaque env

Cible :
1. Créer le dossier `local/myapp/`
2. Initialiser `.wex/config.yml` avec `global.name + tags`
3. `wex master::scan` (ou auto-trigger via watch ?)
   - Détecte la nouvelle app → registre + cache
   - Trouve un `.wex/env/prod/config.yml` → ajoute le host au registre si nouveau
4. Pour rattacher à une stack : `wex master::stack/add tpa myapp` ou éditer `project.yml > stacks > tpa > apps: [..., myapp]`
5. C'est tout.

## Sujets ouverts (à clarifier demain)

- **Watch vs scan manuel ?** Un watcher filesystem (inotify) qui re-enrolle à la volée serait magique, mais ajoute une couche de complexité. Probablement commencer par scan manuel + scheduled.
- **Comment versionner le `apps.yml`** sans en faire un goulot conflictuel ? Au master = oui (c'est l'identité du projet). Au sein du master TPA, ça devrait être ok parce qu'un seul opérateur édite à la fois en pratique.
- **Le cache local (`apps.cache.yml`)** doit-il stocker les paths complets, ou juste un mapping `name → relative_path` ?
- **Comment gérer le `discovered_via`** quand une app a plusieurs envs sur plusieurs hosts ? Liste de provenances ?
- **Intégration avec `master::info/show`** : la commande prend-elle ses données du registre maintenant, ou continue à scanner pour rester en sync ? Probablement registre par défaut + flag `--rescan` pour forcer.
- **Sur quoi se base "une app a disparu"** ? Le path qui n'existe plus ? Le `global.name` plus trouvé dans les apps découvertes ? Cas tordu si on renomme un dossier sans changer le `name`.
- **Le concept de "stack"** mérite d'être enrichi : aujourd'hui c'est juste un groupe nommé d'apps. Avec l'orchestration (#9 de master.md), il faut y mettre l'ordre de dépendance et les contraintes (cf. exemple Syrtis).
- **Compat ascendante** : à la transition, les `apps:` paths actuels doivent continuer à marcher pendant la migration. Mécanisme de bridge.

## Liens

- [master.md](master.md) chantiers #1, #4, #6.5, #8, #9 dépendent ou bénéficient de cette refonte
- [post-tpa-migration-checklist.md](post-tpa-migration-checklist.md) — pas directement lié, mais touche aux mêmes fichiers
