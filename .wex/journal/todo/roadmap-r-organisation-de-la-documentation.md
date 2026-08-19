# Roadmap : Réorganisation de la documentation

Opened: 2026-08-19
Updated: 2026-08-19

# Roadmap : Réorganisation de la documentation

**Lieu unique du chantier.** Tout ce qui concerne le système de documentation se
gère ici. Consolide `.wex/knowledge/state-of-the-art.md` et
`.wex/knowledge/knowledge-system-proposal.md` (supprimés).

Problème de départ : très peu de doc a été écrite, l'auteur s'y perd. On veut une
convention unique appliquée partout, et une doc maintenue le plus automatiquement
possible depuis le code.

**Hors périmètre pour l'instant** : `__summary.md` / `__entrypoint.md` (navigation
générée). Reporté volontairement — la phase 5 décidera du besoin réel.

---

## État de l'art (vérifié dans le code)

**1. Le templating README est déjà bon, juste sous-utilisé.**
Chaîne : `AggregatedTemplatesConfigValue` → `ReadmeContentConfigValue` →
`AppReadmeConfigValue` → `PythonPackageReadmeContentConfigValue`.
Recherche à 4 niveaux (workdir → addon langage → addon app → suites ancêtres),
sections découvertes par fichier `.md.j2`/`.md`, ordre piloté par `readme.sections`
dans le `config.yml` de la suite, rendu Jinja2 avec filtres custom
(`helpers/jinja.py:9`, `ChoiceLoader` multi-chemins).
C'est la brique à généraliser, pas à réécrire.

**2. `AGENTS.md` / `CLAUDE.md` ne sont pas composés.**
`with_ai_workdir_mixin.py:15` — `build_agents_content()` renvoie une chaîne Python
hardcodée ; `CLAUDE.md` est un pointeur d'une ligne (`CLAUDE_POINTER_CONTENT`).
L'intention derrière feu `knowledge/documents/{readme,agents}` était probablement
de les produire depuis des `.j2` : elle est reprise en phase 4.

**3. Reste à déplacer par migration.**
`PACKAGES/PYTHON/.wex/knowledge/todo/` — 7 vrais tickets — doit rejoindre
`.wex/journal/todo/`.

**4. Briques déjà en place.** Commandes `knowledge/read.py`,
`todo/{write,done,list}.py`, `analysis/report.py`, alignées sur
`APP_PATH_JOURNAL_*`. Migrations `6_0_112__2` (roadmap → journal) et
`6_0_130__1` (suppression de `documents/`).

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

## Structure cible de `.wex/knowledge/`

```
knowledge/
├── __entrypoint.md
├── readme/          # fragments .md.j2 → README généré
├── usage/           # utiliser le projet sans le modifier
├── contributing/    # le modifier / l'étendre (humains + agents)
└── specifications/  # référence durable (vision, contraintes, contrats)
```

Au niveau suite s'ajoute `package-readme/` (fragments hérités par les packages
enfants). Nom de compromis, à rebaptiser un jour.

---

## Phase 1 — Structuration des dossiers

- [x] `knowledge/documents/{readme,agents}` supprimé : créé partout, lu par rien.
      La convention qui survit est `knowledge/readme` + `knowledge/package-readme`,
      désormais déclarée dans `managed_workdir.py`
- [x] `coding/` (wex) et `code-style/` (suite) dissous — voir phase 2
- [x] `project/` (wex) et `project-info/` (suite) dissous — voir phase 2
- [x] `tools/` (suite) supprimé
- [ ] Rebaptiser `package-readme/` ?
- [ ] Résidus suite à traiter : `_entrypoint.md` **et** `__entrypoint.md` coexistent ;
      `wex_command_tags.md` traîne à la racine de `knowledge/`

## Phase 2 — Ménage

Réalisé :

- [x] `wex/.wex/knowledge/migration/` supprimé (v5→v6 terminée, 27 fichiers)
- [x] `PACKAGES/PYTHON/.wex/knowledge/roadmap/` supprimé (vide)
- [x] `wex-addon-app/.wex/knowledge/readme/introduction.md` supprimé
      (doublon mort de `introduction.md.j2`)
- [x] `state-of-the-art.md` + `knowledge-system-proposal.md` consolidés ici
- [x] **Obsolètes supprimés (13)** : contenu faux ou vide — `dot-wex-directory.md`
      (décrivait `.wex/bash/` et `.wex/doc/`, disparus), `tools/wex.md` (« Current
      version: 5.x »), `tools/{maintenance-scripts,package-management}.md`
      (documentaient `for_all_package.sh` / `for_all_venv.sh`, scripts inexistants),
      `project-info/{project-conventions,project-structure}.md` (préambule sans
      contenu), et les `_summary.md` / `__summary.md` de l'ancienne convention
- [x] **Déplacés tels quels (6)** : `coding/output.md` → `contributing/output.md`,
      `coding/python/venv.md` → `contributing/venv.md`,
      `project/vision.md` → `specifications/vision.md` (wex) ;
      `project-info/{typed-config-files,app-manager-folder,pip-packages-structure}.md`
      → `contributing/` (suite)
- [x] `project/architecture.md` → `contributing/architecture.md` (wex)

Reste :

- [ ] Migration : `PACKAGES/PYTHON/.wex/knowledge/todo/` → `.wex/journal/todo/`
- [ ] Propager la migration `6.0.130-1` : 84 workdirs portent encore
      `knowledge/documents` (tous vides). Décider du vecteur — commande suite-wide
      ou au fil des `rectify`

## Phase 3 — Rapatrier les règles de code dans le package langage

Supprimés de `wex` et de la suite, **à refaire** dans `wex-addon-dev-python` comme
documentation des options de rectify qui les imposent déjà (`FormatOption`,
`ModernizeTypingOption`, marqueur `# filestate: python-iterable-sort`).
Contenu d'origine récupérable : `wex@7cffc16c4`, suite `@74beedd`.

- [ ] `coding/general.md`, `coding/python/{sorting,spacing,typing,syntax}.md` (wex)
- [ ] `code-style/{general,python,maintenance-script}-code-style.md` (suite)

À réécrire depuis le code, pas à recopier : `python-code-style.md` parlait encore
de Pydantic alors que le code est passé sur attrs / `base_class` / `public_field`.

## Phase 4 — Définir comment se rédige chaque fichier

- [ ] Pour chaque type de fichier : audience, longueur attendue, ton, ce qui y va /
      ce qui n'y va pas, quand il est mis à jour
- [ ] En faire une référence unique et opposable — c'est ce document que liront les
      agents rédacteurs
- [ ] Réécrire `contributing/architecture.md` (30 lignes qui décrivent encore wex
      comme un « Installation Manager », sans un mot sur le kernel, les addons, la
      résolution de commandes)

## Phase 5 — README + templating multi-app

- [ ] Généraliser l'agrégation multi-niveaux à n'importe quelle cible, pas que README
- [ ] Faire produire `AGENTS.md` / `CLAUDE.md` par ce système, depuis des fragments
- [ ] Basculer les fragments `.md` restants en `.j2`
- [ ] Décider si les `.md` exportés sont des artefacts générés versionnés ou non

## Phase 6 — Prompts d'agents à contexte dynamique

- [ ] Définir la composition d'un prompt d'agent : fragments + contexte compilé à la
      volée (structure du projet, dépendances, commandes disponibles…)
- [ ] Réutiliser la même brique d'agrégation que la doc
- [ ] Définir comment les agents cherchent dans la doc, pour eux-mêmes ou pour le USER

## Phase 7 — Enrichir la doc

- [ ] `wex` d'abord, puis module par module, package par package

---

## Pistes à instruire (pas tranchées)

- **Générer la doc depuis le code.** Premier candidat concret : un document décrivant
  l'arborescence `.wex/`, puisque `managed_workdir.prepare_value()` en est la source
  de vérité. Les deux `dot-wex-directory.md` écrits à la main avaient dérivé.
- **Un agent par fichier de doc**, responsable de le maintenir à jour.
- **Commandes de propagation / export** : compilations intelligentes, affichage ciblé.
- **Lier code et doc** : surveiller les diffs, ou tagger les commentaires. Implique
  des cycles de vie de mise à jour.
- **Standard reproductible** : vérifier l'applicabilité hors écosystème Python
  (syrtis, packages PHP/JS).

---

## Statut

Phases 1 et 2 quasi bouclées. `knowledge/` de wex ne contient plus que
`contributing/`, `readme/`, `specifications/`, `usage/` et `__entrypoint.md`.
Rien n'est committé.
Prochaine étape : la migration `knowledge/todo` → `journal/todo`, puis la phase 3.
