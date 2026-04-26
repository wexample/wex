# Knowledge System — Proposal

Proposition généraliste pour la structure et les conventions du système de knowledge, applicable à l'ensemble des projets de l'écosystème wex.

---

## Vision

Un système de knowledge unifié, lisible par les humains, les agents IA et les scripts, qui :
- ne répète jamais une information (DRY, source unique)
- se génère et se maintient en partie automatiquement
- est reproductible sur tout projet géré par wex
- distingue clairement ce qui sert à *utiliser* un projet, à *y contribuer*, et ce qui en définit les *spécifications*

---

## Principes directeurs

1. **Source unique de vérité** — une information n'existe qu'à un endroit. Le reste est généré, importé ou référencé.
2. **Génération > rédaction manuelle** — tout ce qui peut être produit par script ou template doit l'être.
3. **wex comme interface principale** — les agents sont invités à passer par les commandes wex pour explorer et interagir avec le projet. Le knowledge est un cache lisible par les agents qui n'ont pas accès à wex.
4. **Trois axes de lecture** — `usage` / `contributing` / `specifications`, toujours présents quel que soit le type de projet.
5. **Convention avant configuration** — la structure doit être la même partout. Les variantes sont des ajouts, pas des exceptions.
6. **Pas de dossier optionnel** — tous les dossiers sont toujours présents, avec un `.gitkeep` si vide.

---

## Fichiers réservés (convention universelle)

| Fichier | Rôle | Présence |
|---|---|---|
| `__entrypoint.md` | Point d'entrée agent : pourquoi il lit ce dossier, comment naviguer | Racine de `knowledge/` uniquement |

`__entrypoint.md` oriente les agents vers les commandes wex disponibles pour explorer le projet, et explique que le knowledge est un cache de ces données.

---

## Métadonnées

Les métadonnées du projet (structure, index, informations sur les fichiers et dossiers) sont **gérées par wex** et stockées dans un format structuré (YAML ou JSON), soit dans `knowledge/` soit dans un dossier dédié `metadata/`. Elles constituent la source de vérité pour la navigation — les `__summary.md` en sont une représentation lisible dérivée, générée automatiquement par wex.

---

## Fichiers racine du projet (générés)

`README.md`, `AGENTS.md` et `CLAUDE.md` sont tous **générés** par le système filestate.
`AGENTS.md` et `CLAUDE.md` sont deux variantes du même fichier (même source, wrapper différent selon la cible). Leur contenu rejoint celui de `__entrypoint.md` — tous pointent vers les commandes wex comme interface principale.

Les fragments sources sont regroupés dans `knowledge/documents/` :

```
.wex/knowledge/documents/
├── readme/     # fragments → README.md
└── agents/     # fragments → AGENTS.md + CLAUDE.md
```

Le framework de génération agrège des sources à plusieurs niveaux :
```
niveau générique (suite / écosystème)
    +
niveau projet (.wex/knowledge/documents/[type]/)
    =
fichier généré à la racine (jamais édité à la main)
```

Ce même framework doit pouvoir composer n'importe quel type de fichier cible — README, AGENTS, CLAUDE, ou tout autre document — à partir de fragments hétérogènes.

---

## Structure cible de `.wex/knowledge/`

Identique pour tous les types de projets (outil, librairie, application) :

```
.wex/knowledge/
├── __entrypoint.md
├── documents/              # Sources pour les fichiers générés à la racine
│   ├── readme/             # → README.md
│   └── agents/             # → AGENTS.md + CLAUDE.md
├── usage/                  # Comment utiliser le projet
├── contributing/           # Comment modifier / étendre le projet (humains + agents)
├── specifications/         # Specs de référence (CDC digéré, contraintes, domaines)
└── roadmap/
    ├── todo/               # Roadmaps actives
    ├── done/               # Archivé
    └── decisions/          # Tickets de décision (éphémères, tranchés en cours de route)
```

Tous les dossiers sont toujours présents. La densité du contenu varie selon le type de projet, pas la structure.

---

## Les trois axes de lecture

**`usage/`** — pour quelqu'un qui veut utiliser le projet sans le modifier.
Contenu typique : introduction, commandes disponibles, exemples, configuration.

**`contributing/`** — pour quelqu'un (humain ou agent) qui veut modifier ou étendre le projet.
Contenu typique : architecture, conventions de code, processus de contribution, patterns internes.

**`specifications/`** — référence permanente issue du CDC ou des contraintes métier.
Contenu typique : domaines fonctionnels, rôles, parcours utilisateur, contraintes techniques ou réglementaires.
Pour un outil/librairie, peut contenir les specs d'API, les contrats d'interface, les décisions d'architecture durables.

---

## `roadmap/decisions/`

Tickets de décision créés à la volée quand une ambiguïté bloquante est rencontrée.
- Créés par l'agent ou le développeur pendant le travail
- Format : `DOMAINE-NNN-slug.md` (ex: `AUTH-001-session-strategy.md`)
- L'agent documente le contexte, les options, et son choix temporaire
- Le chef de projet tranche, le ticket est mis à jour
- Une fois tranchée et stable, la décision est **distillée** dans `contributing/` ou `specifications/` et le ticket supprimé
- Nature éphémère : `roadmap/decisions/` ne s'accumule pas indéfiniment

---

## Ce qui n'est pas dans ce document

- Le détail de chaque fragment (documents/readme, documents/agents) — traité dossier par dossier
- Le fonctionnement technique du système filestate — déjà en place, à documenter séparément
- Le système de métadonnées wex — à concevoir séparément
- La migration de l'existant — après validation de cette proposition
