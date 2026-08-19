# Roadmap : Réorganisation de la documentation

Opened: 2026-08-19
Updated: 2026-08-19

**Lieu unique du chantier.** Tout ce qui concerne le système de documentation se
gère ici. Consolide `.wex/knowledge/state-of-the-art.md` et
`.wex/knowledge/knowledge-system-proposal.md` (supprimés).

Problème de départ : très peu de doc a été écrite, l'auteur s'y perd. On veut une
convention unique appliquée partout, et une doc maintenue le plus automatiquement
possible depuis le code.

---

## Principes retenus

1. **Source unique de vérité** — une information n'existe qu'à un endroit. Le reste
   est généré, importé ou référencé.
2. **Génération > rédaction manuelle** — ce qui peut être produit par template doit
   l'être. Corollaire appliqué : tout fichier de navigation écrit à la main
   (`__entrypoint.md`, `__summary.md`) est supprimé ; on les regénérera si le besoin
   se confirme.
3. **wex comme interface principale** — les agents passent par les commandes wex
   pour explorer ; le knowledge est le cache lisible pour ceux qui n'y ont pas accès.
4. **Convention avant configuration** — même structure partout ; les variantes sont
   des ajouts, pas des exceptions.
5. **`knowledge/` = intemporel, `journal/` = daté.**

---

## Structure cible de `.wex/knowledge/`

```
knowledge/
├── readme/          # fragments .md.j2 → README généré
├── usage/           # utiliser le projet sans le modifier
├── contributing/    # le modifier / l'étendre (humains + agents)
└── specifications/  # référence durable (vision, contraintes, contrats)
```

Au niveau suite s'ajoute `package-readme/` (fragments hérités par les packages
enfants). Nom de compromis, à rebaptiser un jour.

État atteint dans `wex` — conforme :
`contributing/{architecture,output,venv}.md`, `readme/introduction.md`,
`specifications/vision.md`, `usage/{introduction,testing,webhooks,environment-variables}.md`.

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
de les produire depuis des `.j2` : reprise en phase 5.

**3. Les migrations existent mais ne sont pas propagées.** Constat récurrent :
`6.0.112-2` (roadmap → journal) n'a jamais tourné sur plusieurs packages, et les
deux nouvelles n'ont tourné que sur `wex`.

---

## Les chemins de lecture (inventaire vérifié)

Qui lit le knowledge, par quel mécanisme, et dans quel état. C'est la carte qui
pilote les phases 5 et 6.

**A. `README.md` généré — le seul agrégateur en état de marche.**
`AppReadmeConfigValue`, déclenché au `state/rectify`. Recherche à 4 niveaux, rendu
Jinja2 (détail plus haut). **Sous-alimenté** : ne lit que `readme/`, jamais `usage/`
ni `contributing/` ni `specifications/` ; aucune donnée produite (commandes,
services, packages enfants) n'y entre ; `wex` n'a plus qu'un fragment.
→ Premier cas à traiter.

**B. `AGENTS.md` / `CLAUDE.md` — l'agent qui ne connaît pas wex.**
Chaîne Python hardcodée (`with_ai_workdir_mixin.py:15`), écrite dans chaque workdir,
qui dit désormais « browse `.wex/knowledge/` ». C'est ce qui remplace les
entrypoints/summaries supprimés, et ça ne sait rien du contenu réel du dossier.

**C. L'humain qui ouvre le fichier.** Fonctionne, rien à faire.
Contrainte à graver : **un fragment converti en `.j2` cesse d'être lisible sur
place**. C'est le prix du templating ; à arbitrer dossier par dossier, pas
globalement. Statu quo décidé pour l'instant.

**D. Les agents wex — le trou.** Deux surfaces :
`_knowledge_index()` (`abstract_agent.py:677`) liste des identifiants
`<service>:<section>` dans le system prompt sans lire le contenu ; `app::knowledge/read`
(`AGENT_SAFE`) résout `find_service_dir()` puis lit `<service_dir>/knowledge/<section>.md`
en texte brut, sans rendu de template.
**Les deux ne visent que le knowledge des *services*. Le `.wex/knowledge/` de l'app
elle-même n'a aucun chemin de lecture programmatique** — un agent ne peut pas
atteindre `contributing/architecture.md`.
À côté, la cascade `context.j2` (5 niveaux, `abstract_agent.py:444-558`) est le seul
précédent de contexte compilé au moment de la lecture, mais elle ne rend que les
fichiers littéralement nommés `context.j2` (`_render_context_template():1335`) et
n'injecte jamais de knowledge.

**E. `journal/todo|done` — le seul circuit complet.**
`todo/write|done|list` sont `HUMAN_ONLY` **délibérément** (`todo/write.py:45`) : les
agents y accèdent par les outils `todo_write`/`todo_list`, qui gèrent en plus la pile
de sujets. `analysis/report` est le pendant `AGENT_SAFE`, en écriture vers
`journal/analysis/`.
**Il y a donc deux surfaces d'exposition distinctes** — commandes MCP filtrées par
tags, et outils d'agent dédiés — à ne pas confondre en phase 6.

**Ce que la carte montre** : un agrégateur (A) et un circuit agent complet (E), et
entre les deux un trou (D). Traiter A proprement force à définir la brique
réutilisable — résolution multi-niveaux + rendu j2 + injection de données produites —
dont B et D ont besoin.

---

## Phase 1 — Structuration des dossiers ✅

- [x] `knowledge/documents/{readme,agents}` supprimé : créé partout, lu par rien.
      La convention qui survit est `knowledge/readme` + `knowledge/package-readme`,
      désormais déclarée dans `managed_workdir.py`
- [x] `coding/` + `code-style/`, `project/` + `project-info/`, `tools/` dissous
- [x] `__entrypoint.md` retiré de la déclaration filestate (créé vide dans 82
      workdirs) et supprimé
- [x] `__summary.md` / `_summary.md` supprimés — la référence dans `AGENTS.md`
      (`with_ai_workdir_mixin.py:32`) pointait vers un fichier qui n'existait
      quasiment nulle part, remplacée par « browse `.wex/knowledge/` »
- [ ] Rebaptiser `package-readme/` ?

## Phase 2 — Ménage

Réalisé dans `wex` et la suite `PACKAGES/PYTHON` :

- [x] `knowledge/migration/` supprimé (v5→v6 terminée, 27 fichiers)
- [x] **Obsolètes supprimés** : `dot-wex-directory.md` (décrivait `.wex/bash/` et
      `.wex/doc/`, disparus), `tools/wex.md` (« Current version: 5.x »),
      `tools/{maintenance-scripts,package-management}.md` (documentaient
      `for_all_package.sh` / `for_all_venv.sh`, scripts inexistants),
      `project-info/{project-conventions,project-structure}.md` (vides de contenu),
      `contributing/exporting-skeleton.md` (procédure de duplication en `_copy`,
      ancienne convention)
- [x] `wex_command_tags.md` supprimé — sortie d'agent de 385 lignes dont 233
      d'inventaire des commandes, périmé au premier ajout. **La section 3 est une
      taxonomie de tags proposée et non appliquée** ; les tags servent déjà au
      filtrage MCP (`DEFAULT_EXCLUDED_TAGS = {"human-only"}`,
      `wex-addon-ai/helpers/mcp.py`). À récupérer pour la phase 6 : `suite@99e98dd`
- [x] **Déplacés** : `coding/output.md` → `contributing/`, `coding/python/venv.md`
      → `contributing/`, `project/vision.md` → `specifications/`,
      `project/architecture.md` → `contributing/` (wex) ;
      `project-info/{typed-config-files,app-manager-folder,pip-packages-structure}.md`
      → `contributing/` (suite)

Reste :

- [ ] Migration : `PACKAGES/PYTHON/.wex/knowledge/todo/` → `.wex/journal/todo/` (7 tickets)
- [ ] Propager les migrations `6.0.130-1` (suppression `documents/`) et `6.0.130-2`
      (suppression `__entrypoint.md`) : ~84 workdirs, tous vides. Décider du vecteur —
      commande suite-wide ou au fil des `rectify`
- [ ] Knowledge pollués des autres packages : un par un, hors de ce chantier.
      Cas le plus lourd repéré : `packages/filestate/.wex/doc/` (vestige v5) contient
      498 lignes de fragments README orphelins, tandis que son `README.md` (477 lignes)
      est figé et non régénérable

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

Premier cas de lecture traité (cas A), et prétexte à extraire la brique commune.

- [ ] Remettre le README de `wex` en état : aujourd'hui un seul fragment
- [ ] Décider ce qui alimente le README au-delà de `readme/` — sections tirées de
      `usage/` / `specifications/` ? références seulement ?
- [ ] Injecter des données produites : commandes, services, packages enfants
- [ ] Généraliser l'agrégation multi-niveaux à n'importe quelle cible, pas que README
- [ ] Faire produire `AGENTS.md` / `CLAUDE.md` par ce système (cas B)
- [ ] Ouvrir un chemin de lecture sur le `.wex/knowledge/` de l'app (cas D)
- [ ] Basculer les fragments `.md` restants en `.j2` — arbitrer avec le cas C
- [ ] Décider si les `.md` exportés sont des artefacts générés versionnés ou non

## Phase 6 — Prompts d'agents à contexte dynamique

- [ ] Définir la composition d'un prompt d'agent : fragments + contexte compilé à la
      volée (structure du projet, dépendances, commandes disponibles…)
- [ ] Réutiliser la même brique d'agrégation que la doc
- [ ] Reprendre la taxonomie de tags (`suite@99e98dd`) pour le filtrage MCP
- [ ] Définir comment les agents cherchent dans la doc, pour eux-mêmes ou pour le USER

## Phase 7 — Enrichir la doc

- [ ] `wex` d'abord, puis module par module, package par package

---

## Pistes à instruire (pas tranchées)

- **Générer la doc depuis le code.** Premier candidat concret : un document décrivant
  l'arborescence `.wex/`, puisque `managed_workdir.prepare_value()` en est la source
  de vérité. Les deux `dot-wex-directory.md` écrits à la main avaient dérivé.
  Deuxième candidat : l'inventaire des commandes, cf. `wex_command_tags.md`.
- **Un agent par fichier de doc**, responsable de le maintenir à jour.
- **Commandes de propagation / export** : compilations intelligentes, affichage ciblé.
- **Lier code et doc** : surveiller les diffs, ou tagger les commentaires. Implique
  des cycles de vie de mise à jour.
- **Standard reproductible** : vérifier l'applicabilité hors écosystème Python
  (syrtis, packages PHP/JS).

---

## Statut

Phase 1 bouclée, phase 2 bouclée pour `wex` et la suite Python. Le `knowledge/` de
wex est conforme à la structure cible (13 fichiers, 4 dossiers).
Les chemins de lecture sont inventoriés et vérifiés dans le code.
Rien n'est committé.
Prochaine étape : phase 5, cas A (README de `wex`), qui sert de banc d'essai à la
brique d'agrégation réutilisable.
