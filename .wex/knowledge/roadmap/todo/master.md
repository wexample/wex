# Roadmap master post-migration wex 6

## Contexte

Wexample / Syrtis / TPA sont passés en wex 6 (mai 2026). Première passe terminée — toutes les apps tournent. Reste à consolider l'outillage master + remettre le CI/CD TPA debout + faire le ménage côté services self-hosted.

## Chantiers

### 1. Intégrer les remotes manquantes au master

- **TPA dev** ✅ fait (`wex master::info/show --remotes dev` montre tpa)
- **Runner wex** ⏳ pas fait — runner CI/CD à exposer comme remote master pour le piloter/observer depuis le dashboard. Rsync local à `/home/weeger/Desktop/WIP/WEB/TPA/local/runner/` pour inspection.

Spec : que `wex master::info/show --remotes <name>` montre Local Version / Wex / Git pour chaque app sur la remote.

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

### 6.5. `wex upgrade` partout

Aujourd'hui faisable manuellement : `for srv in ...; do ssh weeger@$srv "wex upgrade"; done`. Fait pour 4 serveurs en 6.0.104 le 2026-05-28.

À industrialiser : `wex master::servers/upgrade` qui ssh sur chaque remote (déclaré dans les remotes des apps connues), exécute `apt update && apt install -y wex`, rapporte version avant/après par host. Bonus : check de compatibilité (si le CLI passe à 6.X.Y, les apps stampées à 6.X-1.Z doivent rester compatibles ou être migrées en même temps).

Pré-requis : avoir un registre des hosts au niveau master (cf. friction #8 ci-dessous).

### 7. Commandes de maintenance des apps

Set d'opérations cross-env qu'on fait à la main aujourd'hui et qu'on devrait pouvoir scripter :

- **Sync data prod → dev** : dump BDD prod, restore en dev (cas typique : tester une migration sur des données réelles, refresh un staging stale)
- **Sync data dev → prod** : plus rare mais utile pour seed initial
- **Backup ponctuel** : déclencher un backup nommé (avant migration risquée), pas le cron auto
- **Restore depuis backup** : sélectionner un backup, restore-le dans un env donné

Pré-requis : chaque app/service doit savoir décrire ses "ressources persistantes" (BDD, volumes, secrets) et exposer ses primitives dump/restore. Cf. chantier (5) — déjà touché pour les updates de service.

Spec ergonomique cible : `wex app::data/sync --from prod --to dev` (ou similaire).

### 8. Master "host registry" + provisioning éphémère

Aujourd'hui les `host:` (IPs) sont déclarés **par app, par env, dans `.wex/env/<env>/config.yml`**. Pas de registre central. Pour ajouter un env ou changer une IP, il faut éditer N fichiers d'apps. Friction relevée plusieurs fois pendant la session du 2026-05-28 (intégration dev TPA, déploiement plausible).

À ajouter dans `master.local.yml` :
```yaml
hosts:
  tpa_prod: 51.210.104.199
  tpa_dev: 152.228.175.159
  wexample_prod: 151.80.23.108
  syrtis_prod: 79.137.89.25
```
Et permettre aux apps de référencer : `remotes[].host: ${HOST_TPA_PROD}`.

**Pré-requis du chantier `wex upgrade partout` (#6.5) ET du provisioning éphémère (#9).**

### 9. Master orchestration & auto-provisioning

Discussion 2026-05-28. La promesse de fond : depuis le master, **provisionner / déployer / détruire** des environnements complets en une commande, sur des hosts éphémères payés à l'usage. Triple use case.

#### Use case A — Démos client / staging temporaire

User planifie ses démos. À T-10 min, lance `wex master::stack/deploy --stack tpa --remote demo-laurius`. Le master :
1. Provisionne un host via API cloud
2. Cloud-init/ansible minimal le rend prêt (wex CLI, Docker daemon, network)
3. DNS éphémère `demo-laurius.thephotoacademy.com` via Cloudflare API (provider qu'on vient d'implémenter)
4. Pull la stack TPA depuis git, `wex app::app/start --remote` chaque app
5. Snapshot DB seedée (cf. chantier #7)
6. Renvoie l'URL démo

Après démo, `wex master::stack/destroy --remote demo-laurius` → DNS supprimé + host détruit. Coût total : ~0,05€ par démo de 2h sur Hetzner.

#### Use case B — Runner CI/CD éphémère

Le runner à 80€/mois dort 23h/jour. Alternative : un manager runner permanent minuscule (~3€/mois) qui, à chaque pipeline lourd, demande un host ad-hoc, run le job, détruit. Mécanique standard côté GitLab = fleeting plugin (`fleeting-plugin-aws`, `fleeting-plugin-hetzner`) — pas besoin de réinventer, juste de l'intégrer au master pour piloter les credentials et le scaling depuis un endroit unique.

Trade-off de latence : cold-start ~30s (Hetzner) à 1-2 min (OVH). Optim possible via **template/snapshot pré-cuit** (Docker + outils déjà installés) → cold-start réduit à ~30s. Packer + Hetzner snapshots, ou OVH Public Cloud images custom.

#### Use case C — Déploiement Syrtis (stack multi-services interdépendants)

Le stretch initial. Maintenant éclairé par les deux précédents : si on sait spawn un host + déployer N apps qui s'attendent (postgres avant api avant manager…), on sait déployer Syrtis. La primitive "stack" doit gérer **les dépendances inter-apps** (cf. `stacks:` dans `project.yml` qui existe déjà mais sert juste à grouper, pas à orchestrer).

#### Briques techniques (à étudier)

| Brique | Choix par défaut | Alternative |
|---|---|---|
| Cloud provider | Hetzner Cloud (best price/perf EU, ~5€/mois équivalent OVH 80€) | OVH Public Cloud (rester en France), Scaleway, AWS EC2 Spot (worldwide top) |
| Provisioning infra | Terraform (déclare ce qui existe) | OpenTofu, Pulumi, ou direct API client Python |
| Provisioning host | Cloud-init via user-data | Ansible (plus puissant mais plus lourd) |
| Template host | Packer pour pré-cuire snapshot (Docker + wex CLI déjà installés) | Cloud-init from-scratch à chaque fois (1-2 min cold-start) |
| DNS éphémère | Cloudflare API (provider déjà implémenté) | Manuel via UI (pas scalable) |
| Pipeline CI runner | GitLab Runner Autoscaler + fleeting-plugin-hetzner | BuildJet/Buildkite (SaaS, mais oblige à quitter GitLab CI) |

#### Découpage en sous-chantiers

1. **Host registry au master** — pré-requis (chantier #8 ci-dessus) : déclarer les hosts au niveau master, les apps les référencent par nom
2. **Provider abstrait `HostProvider`** dans wex-addon-master, comme on a fait pour DNS — implem Hetzner d'abord
3. **`wex master::host/spawn --provider hetzner --type cpx21`** → returns IP, ssh OK
4. **`wex master::host/destroy <name>`** → symétrique
5. **`wex master::stack/deploy --stack <name> --remote <host>`** → boucle sur apps de la stack en respectant l'ordre de dépendance
6. **DNS éphémère** → wrapper Cloudflare provider pour create A record + cleanup
7. **Use case B (CI runner)** — intégration fleeting-plugin-hetzner via le manager runner
8. **Templating / Packer image** — accélère cold-start
9. **Use case A (démo)** — combine spawn + DNS + deploy en une commande
10. **Use case C (Syrtis)** — applique le pattern à la stack Syrtis

Ce sera probablement un chantier de plusieurs semaines. Approche incrémentale : commencer par 1+2+3 (provisionner un host vide depuis le master), puis ajouter les couches.

### 10. Nouveaux services à installer

- ✅ **Plausible TPA** (`plausible.thephotoacademy.com`) — déployé sur prod 2026-05-28
- ⏳ **Plausible Wex** — analytics web pour le pôle Wexample
- ⏳ **PostHog** sur Syrtis (analytics produit)
- ⏳ **OpenClaw #2** sur Syrtis pour Gabriel
- ⏳ **OpenClaw #3** sur Syrtis pour Simon

Chaque install = nouvelle app wex 6, à monter selon le template standard.

## Refonte architecturale en cours d'élaboration

Un chantier transverse de **refonte du master** est en cours de design — il englobe plusieurs frictions structurelles (host registry #8 inclus, mais aussi : apps autodescriptives par nom et tags, stacks par nom ou tag plutôt que par path, registre d'apps, auto-enrollment, etc.). Document dédié : [master-architecture-refactor.md](master-architecture-refactor.md).

À traiter avant ou en parallèle de (4), (5), (6), (6.5), (8), (9) — ce sont tous des chantiers qui bénéficient ou dépendent de la refonte.

## Notes

- Liste non-exhaustive — à étoffer au fil de l'eau
- Priorité par défaut : (2) CI/CD TPA d'abord (bloquant pour la prod TPA au quotidien, agent dédié déjà briefé via [ci-cd-agent-brief.md](/home/weeger/Desktop/WIP/WEB/TPA/local/tpa/.wex/knowledge/ci-cd-agent-brief.md)), puis la refonte master ([master-architecture-refactor.md](master-architecture-refactor.md)) qui débloque le reste, puis (1) runner remote, puis (4)/(5)/(7) outillage, puis (3) updates et (10) nouveaux services en parallèle.
