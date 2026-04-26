# Knowledge System — Proposal

Proposition généraliste pour la structure et les conventions du système de knowledge, applicable à l'ensemble des projets de l'écosystème wex.

---

## Vision

Un système de knowledge unifié, lisible par les humains, les agents IA et les scripts, qui :
- ne répète jamais une information (DRY, source unique)
- se génère et se maintient en partie automatiquement
- est reproductible sur tout projet géré par wex
- distingue clairement ce qui sert à *utiliser* un projet de ce qui sert à *y contribuer*

---

## Principes directeurs

1. **Source unique de vérité** — une information n'existe qu'à un endroit. Le reste est généré, importé ou référencé.
2. **Génération > rédaction manuelle** — tout ce qui peut être produit par script ou template doit l'être.
3. **Navigabilité par les agents** — chaque dossier doit permettre à un agent de savoir ce qu'il contient sans tout lire.
4. **Deux axes de lecture** — usage (je veux utiliser) vs contribution (je veux modifier). Les deux audiences incluent les humains ET les agents IA.
5. **Convention avant configuration** — la structure doit être la même partout. Les variantes sont des ajouts, pas des exceptions.

---

## Fichiers réservés (convention universelle)

| Fichier | Rôle | Présence |
|---|---|---|
| `__entrypoint.md` | Point d'entrée agent : pourquoi il lit ce dossier, comment naviguer | Racine de `knowledge/` uniquement |
| `__summary.md` | Index du dossier courant : liste et décrit chaque fichier/sous-dossier | Dans chaque dossier |

Ces deux fichiers sont **générés ou maintenus par convention stricte** — jamais rédigés librement.

---

## Fichiers racine du projet

`README.md`, `AGENTS.md` et `CLAUDE.md` sont tous les trois **générés** par le système filestate, par concaténation de fragments provenant de plusieurs niveaux :

```
niveau générique (suite / écosystème)
    +
niveau projet (.wex/knowledge/readme/, .wex/knowledge/agents/, .wex/knowledge/claude/)
    =
README.md / AGENTS.md / CLAUDE.md  (générés, jamais édités à la main)
```

Chaque fichier a son propre dossier de fragments dans `knowledge/` :
- `readme/` → `README.md`
- `agents/` → `AGENTS.md`
- `claude/` → `CLAUDE.md`

---

## Structure cible de `.wex/knowledge/`

### Dossiers universels (tous types de projets)

```
.wex/knowledge/
├── __entrypoint.md
├── __summary.md
├── decisions/              # ADR — choix techniques et ambiguïtés tranchées
├── roadmap/
│   ├── todo/               # Roadmaps actives (lu par les agents)
│   └── done/               # Archivé (ignoré par les agents)
├── readme/                 # Fragments → README.md
├── agents/                 # Fragments → AGENTS.md
└── claude/                 # Fragments → CLAUDE.md
```

### Dossiers selon le type de projet

**Projet outil / librairie / package** (ex : `wex`, packages Python/PHP/JS) :

```
├── usage/                  # Comment utiliser l'outil
│   ├── introduction.md
│   ├── commands.md
│   └── ...
└── contributing/           # Comment modifier / étendre l'outil
    ├── architecture.md
    ├── coding/             # Conventions de code (si non couvertes par filestate)
    └── ...
```

**Projet applicatif** (ex : `mojoe`, `sapiens-react`) :

```
├── specifications/         # Specs issues du CDC, structurées par domaine
│   ├── description/
│   ├── access_roles/
│   ├── data/
│   ├── user_journeys/
│   └── ...
└── contributing/           # Architecture technique, conventions de dev
```

Les deux types partagent `decisions/`, `roadmap/`, et les dossiers de fragments générés.

---

## Le dossier `decisions/`

Pattern ADR adapté à la collaboration agent/humain.

- Un fichier par décision, nommé `DOMAINE-NNN-slug.md` (ex: `AUTH-001-session-strategy.md`)
- Créé par l'agent dès qu'il rencontre une ambiguïté bloquante ou un choix structurant
- L'agent documente le contexte, les options, et son choix temporaire
- Le chef de projet tranche, le fichier est mis à jour et reste comme référence

Ce dossier ne va jamais dans `done/` — les décisions restent consultables indéfiniment.

---

## Le dossier `roadmap/`

- `todo/` : roadmaps actives, lues par les agents. Un fichier = une mission phasée avec cases à cocher.
- `done/` : roadmaps terminées, archivées. Les agents n'ont pas besoin d'y aller.
- Quand tous les items d'un fichier `todo/` sont cochés, il est déplacé dans `done/` ou supprimé.

---

## Maintenance des `__summary.md`

Question ouverte — trois approches possibles, à décider :

1. **Script wex** : commande qui régénère tous les `__summary.md` d'un projet à la demande.
2. **Convention agent** : tout agent qui crée ou modifie un fichier met à jour le `__summary.md` du dossier concerné.
3. **Hybride** : le script fait la génération initiale et structurelle, les agents font les mises à jour incrémentales.

---

## Ce qui n'est pas dans ce document

- Le détail de chaque fichier fragment (readme, agents, claude) — traité dossier par dossier
- Le fonctionnement technique du système filestate — déjà en place, à documenter séparément
- La migration de l'existant — après validation de cette proposition
