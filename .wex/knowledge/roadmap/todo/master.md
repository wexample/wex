# Roadmap master post-migration wex 6

## Contexte

Wexample / Syrtis / TPA sont passés en wex 6 (mai 2026). Première passe terminée — toutes les apps tournent. Reste à consolider l'outillage master + remettre le CI/CD TPA debout + faire le ménage côté services self-hosted.

## Chantiers

### 1. Intégrer les remotes manquantes au master

Aujourd'hui le master TPA voit `prod`. Manquent :

- **TPA dev** — environnement intermédiaire avant prod, doit apparaître dans `wex master::info/show --remotes dev`
- **Runner wex** — runner CI/CD, à exposer comme remote master pour qu'on puisse le piloter / observer depuis le dashboard

Spec : que `wex master::info/show --remotes <name>` montre Local Version / Wex / Git pour chaque app sur la remote, comme pour prod aujourd'hui.

### 2. Remettre le CI/CD TPA en état (version moderne)

Les builds sont historiquement très lents. Objectifs :

- Faire passer les pipelines TPA sur la nouvelle stack wex 6 (push direct fonctionne déjà depuis la migration manuelle, mais les jobs gitlab-ci doivent suivre)
- Chercher des optims sur les temps de build (cache layers Docker, multi-stage, BuildKit, registry mirror, base images pré-cuites…)
- Critère : un commit sur `master` doit déployer en dev en < X min (à fixer après baseline)

### 3. Mise à jour de toutes les apps self-hosted

Passer chaque service à sa dernière stable :

- gitlab-ce (actuellement pin `17.6.1-ce.0`)
- listmonk
- baserow
- matomo
- n8n
- postgres / mysql (par service)
- nginx-proxy / acme-companion

Pour chaque app : check changelog → bump image → tester en local/dev → push prod.

### 4. Améliorer `wex master::info/*`

Commande dashboard à enrichir :

- Versions **services** (image docker + tag) par app, pas seulement version de l'app
- Vue **multi-env** : prod + dev + local côte à côte
- Diff explicite quand un env est en retard sur un autre
- Indicateur "update disponible" (compare avec dockerhub)

### 5. Workflow "update service"

Une commande type `wex app::service/update <service>` qui :

1. Backup spécifique au service (gitlab-backup, n8n export, mysqldump, pg_dump… chacun son protocole)
2. Fetch dernière version sur dockerhub (ou tag spécifié)
3. Apply (rebuild + restart)
4. Commit + push la bump de version
5. Pull + apply sur tous les autres envs (dev → prod)

Cible : zéro étape manuelle, zéro oubli de backup.

### 6. Workflow "tout à jour en N commandes"

Vision : depuis le master, en quelques commandes :

- Toutes les apps wex à jour (wex CLI)
- Tous les envs à jour
- Tous les services self-hosted à leur dernière stable

Ça vient naturellement une fois (1), (4), (5) en place.

### 7. (Stretch) Déploiement Syrtis en wex 6

Syrtis n'est pas encore déployable via wex 6 — c'est un déploiement de stack (multi-services interdépendants), pas une app simple. Étudier :

- Comment wex 6 gère une stack (vs une app)
- Quelles primitives manquent
- Roadmap dédié si confirmé

### 8. Nouveaux services à installer

- **PostHog** sur Syrtis (analytics produit)
- **OpenClaw #2** sur Syrtis pour Gabriel
- **OpenClaw #3** sur Syrtis pour Simon
- **Plausible** pour TPA et Wex (analytics web)

Chaque install = nouvelle app wex 6, à monter selon le template standard.

## Notes

- Liste non-exhaustive — à étoffer au fil de l'eau
- Priorité par défaut : (2) CI/CD TPA d'abord (bloquant pour la prod TPA au quotidien), puis (1) remotes, puis (4)/(5) outillage, puis (3) updates et (8) nouveaux services en parallèle
