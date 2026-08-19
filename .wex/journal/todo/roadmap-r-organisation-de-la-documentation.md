# Roadmap : Réorganisation de la documentation

Opened: 2026-08-19
Updated: 2026-08-19

# Roadmap : Réorganisation de la documentation

**Lieu unique du chantier.** Tout ce qui concerne le système de documentation se
gère ici. Consolide et remplace `.wex/knowledge/state-of-the-art.md` et
`.wex/knowledge/knowledge-system-proposal.md` (supprimés).

Problème de départ : très peu de doc a été écrite, l'auteur s'y perd. On veut une
convention unique appliquée partout, et une doc maintenue le plus automatiquement
possible depuis le code.

**Hors périmètre pour l'instant** : `__summary.md` / `__entrypoint.md` (navigation
générée). Reporté volontairement — la façon dont les agents cherchent dans la doc
(phase 5) décidera du besoin réel.

---

## État de l'art (vérifié dans le code)

**1. `knowledge/documents/` est mort-né.**
`managed_workdir.py:762+` déclare et fait créer `knowledge/documents/readme/` et
`knowledge/documents/agents/` (avec `.gitkeep`) dans **tous** les workdirs. Aucun
code ne les lit. Les fragments réellement consommés sont ailleurs :
`AppReadmeConfigValue._get_readme_search_paths()` (`app_readme_config_value.py:111`)
cherche dans `knowledge/readme/` (workdir) et `knowledge/package-readme/` (suites).
Deux conventions concurrentes : la déclarée est vide, la réelle n'est pas déclarée.

**2. `AGENTS.md` / `CLAUDE.md` ne sont pas composés.**
`with_ai_workdir_mixin.py:15` — `build_agents_content()` renvoie une chaîne Python
hardcodée ; `CLAUDE.md` est un pointeur d'une ligne (`CLAUDE_POINTER_CONTENT`).
Rien ne vient de `knowledge/documents/agents/`, alors que le mécanisme
d'agrégation existe déjà et saurait les produire.

**3. Le templating README est déjà bon, juste sous-utilisé.**
Chaîne : `AggregatedTemplatesConfigValue` → `ReadmeContentConfigValue` →
`AppReadmeConfigValue` → `PythonPackageReadmeContentConfigValue`.
Recherche à 4 niveaux (workdir → addon langage → addon app → suites ancêtres),
sections découvertes par fichier `.md.j2`/`.md`, ordre piloté par `readme.sections`
dans le `config.yml` de la suite, rendu Jinja2 avec filtres custom
(`helpers/jinja.py:9`, `ChoiceLoader` multi-chemins).
C'est la brique à généraliser, pas à réécrire.

**4. Doublons de dossiers entre `wex` et la suite.**
`wex/.wex/knowledge/coding/` (9 fichiers) recouvre
`PACKAGES/PYTHON/.wex/knowledge/code-style/` ; `wex/.wex/knowledge/project/`
recouvre `PACKAGES/PYTHON/.wex/knowledge/project-info/`. S'ajoute `tools/` au
niveau suite, hors modèle. Aucun de ces dossiers n'est dans la structure cible.

**5. Reste à déplacer par migration.**
`PACKAGES/PYTHON/.wex/knowledge/todo/` — 7 vrais tickets — doit rejoindre
`.wex/journal/todo/`. À traiter par une migration, pas à la main.

**6. Briques déjà en place.** Commandes `knowledge/read.py`,
`todo/{write,done,list}.py`, `analysis/report.py`, toutes alignées sur
`APP_PATH_JOURNAL_*`. Migration `roadmap` → `journal` :
`migration_6_0_112__2.py`.

---

## Principes retenus

1. **Source unique de vérité** — une information n'existe qu'à un endroit. Le reste
   est généré, importé ou référencé.
2. **Génération > rédaction manuelle** — ce qui peut être produit par template doit l'être.
3. **wex comme interface principale** — les agents passent par les commandes wex
   pour explorer ; le knowledge est le cache lisible pour ceux qui n'y ont pas accès.
4. **Convention avant configuration** — même structure partout ; les variantes sont
   des ajouts, pas des exceptions.
5. **`knowledge/` = intemporel, `journal/` = daté.**

---

## Phase 1 — Valider la structuration des dossiers

Trancher la cible et l'écrire une fois pour toutes.

- [ ] Arbitrer `knowledge/documents/{readme,agents}` **vs** `knowledge/readme` +
      `knowledge/package-readme` : une seule convention survit, l'autre disparaît du code
- [ ] Décider du nom au niveau suite (`package-readme` est un nom de compromis)
- [ ] Trancher `coding/` (wex) vs `code-style/` (suite) : lequel survit, où il vit
- [ ] Trancher `project/` (wex) vs `project-info/` (suite), et le sort de `tools/`
- [ ] Vérifier la frontière `knowledge/` / `journal/` pour chaque dossier restant
- [ ] Aligner `managed_workdir.py` : ce qui est déclaré doit être lu

## Phase 2 — Ménage

- [x] Supprimer `wex/.wex/knowledge/migration/` (v5→v6 terminée, 27 fichiers)
- [x] Supprimer `PACKAGES/PYTHON/.wex/knowledge/roadmap/` (vide, 3 `.gitkeep`)
- [x] Supprimer `wex-addon-app/.wex/knowledge/readme/introduction.md`
      (doublon mort de `introduction.md.j2`)
- [x] Consolider `state-of-the-art.md` + `knowledge-system-proposal.md` ici
- [ ] Migration : `PACKAGES/PYTHON/.wex/knowledge/todo/` → `.wex/journal/todo/`
- [ ] Appliquer les arbitrages de la phase 1 (déplacements / suppressions restants)

## Phase 3 — Définir comment se rédige chaque fichier

- [ ] Pour chaque type de fichier : audience, longueur attendue, ton, ce qui y va /
      ce qui n'y va pas, quand il est mis à jour
- [ ] En faire une référence unique et opposable — c'est ce document que liront les
      agents rédacteurs

## Phase 4 — README + templating multi-app

- [ ] Généraliser l'agrégation multi-niveaux à n'importe quelle cible, pas que README
- [ ] Faire produire `AGENTS.md` / `CLAUDE.md` par ce système, depuis des fragments
- [ ] Basculer les fragments `.md` restants en `.j2`
- [ ] Décider si les `.md` exportés sont des artefacts générés versionnés ou non

## Phase 5 — Prompts d'agents à contexte dynamique

- [ ] Définir la composition d'un prompt d'agent : fragments + contexte compilé à la
      volée (structure du projet, dépendances, commandes disponibles…)
- [ ] Réutiliser la même brique d'agrégation que la doc
- [ ] Définir comment les agents cherchent dans la doc, pour eux-mêmes ou pour le USER

## Phase 6 — Enrichir la doc

- [ ] `wex` d'abord, puis module par module, package par package

---

## Pistes à instruire (pas tranchées)

- **Un agent par fichier de doc**, responsable de le maintenir à jour.
- **Commandes de propagation / export** : compilations intelligentes, affichage ciblé.
- **Lier code et doc** : surveiller les diffs du code, ou tagger les commentaires,
  pour que la doc se maintienne « magiquement ». Implique des cycles de vie de mise à jour.
- **Standard reproductible** : vérifier l'applicabilité hors écosystème Python
  (syrtis, packages PHP/JS).

---

## Statut

Phase 2 entamée (suppressions faites, migration `knowledge/todo` restante).
Prochaine étape bloquante : les arbitrages de la **phase 1**, à faire avec le USER.
