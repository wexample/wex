# Knowledge System — State of the Art

Consignement de l'état actuel du système de knowledge, des conventions existantes, des patterns observés sur différents projets, et des problèmes identifiés. Ce document précède toute prise de décision.

---

## Contexte général

`wex` est le CLI Python central de l'écosystème. Le dossier `.wex/` et sa convention `knowledge/` ont vocation à devenir un standard appliqué à tous les projets gérés par wex (outils, packages, applications). L'enjeu est donc double : bien définir le système pour `wex` lui-même, et s'assurer qu'il soit reproductible ailleurs.

---

## Conventions existantes dans `.wex/knowledge/`

### Fichiers réservés

- **`__entrypoint.md`** — point d'entrée pour les agents IA. Explique pourquoi l'agent lit ce dossier et ce qu'il doit faire. Un seul par projet, à la racine de `knowledge/`.
- **`__summary.md`** (anciennement `_summary.md`) — présent dans chaque dossier, liste et décrit son contenu. Permet à un agent de naviguer sans tout lire. Problème : se désynchronise facilement, sa maintenance est un sujet ouvert.

### Dossiers actuels dans `wex`

| Dossier | Statut | Commentaire |
|---|---|---|
| `coding/` | Peu utilisé | Conventions de code Python. Pertinent pour la contribution (humains et agents), mais jamais vraiment activé. Les scripts de rectification (filestate) ont pris le relais. À reconsidérer. |
| `contributing/` | Existant | Contribution au projet. À aligner avec la distinction usage/contribution. |
| `migration/` | Temporaire | Créé pour le passage v5→v6. Hors modèle, à supprimer quand les checks restants sont faits. |
| `project/` | Partiel | Tentative de documentation du projet (architecture, vision, dot-wex-directory). Peu élaboré. Contient encore l'ancienne convention `_summary.md`. |
| `readme/` | En place | Fragments de README destinés à la génération automatique (système filestate). |
| `roadmap/` | Actif | Roadmaps de travail avec `todo/` et `done/`. Utilisé activement en collaboration agent/humain. |
| `todo/` | Actif | Tâches ponctuelles hors roadmap. |

---

## Fichiers racine du projet

| Fichier | État actuel | Problème |
|---|---|---|
| `README.md` | Contenu présent mais désorganisé | Version hardcodée, mélange installation / tests / webhooks, pas de structure claire. Devrait être généré. |
| `AGENTS.md` | Quasi vide (une ligne) | Non exploité. Devrait être généré ou structuré. |
| `CLAUDE.md` | Quasi vide (une ligne) | Idem. |

---

## Patterns observés sur d'autres projets

### `wex-addon-app` + suite PYTHON — Génération de README

Système filestate : le README est généré par concaténation de fragments.
- Fragments locaux au projet : `.wex/knowledge/readme/`
- Fragments hérités de la suite parente : `PACKAGES/PYTHON/.wex/knowledge/package-readme/`
- Classes Python impliquées : `readme_content_config_value.py`, `app_readme_config_value.py`

Principe : **une seule source de vérité**, le reste est copié/importé. Pas de répétition d'une affirmation à plusieurs endroits.

### `mojoe` — Knowledge orienté production d'application

Pas de `.wex/knowledge/`, tout à plat à la racine. Fichiers YAML structurés par domaine :
`features.yaml`, `forms.yaml`, `roles.yaml`, `user_stories.yaml`, `database.yaml`, etc.
Un fichier `__generate.md` indique une logique de génération depuis ces specs.
Pattern : le CDC est découpé en specs consommables par des agents pour produire une application.

### `sapiens-react` — Decisions + Specifications

**`decisions/`** : tickets de décision créés à la volée par l'agent quand quelque chose est flou dans le CDC. Format `DOMAINE-NNN-slug.md` (ex: `AUTH-001`, `DB-002`). L'agent fait un choix temporaire et ouvre le ticket ; le chef de projet tranche plus tard. Proche du pattern ADR (Architecture Decision Record).

**`specifications/`** : digestion du CDC en specs structurées par domaine (`access_roles`, `data`, `user_journeys`, `wireframes`, `rgpd`…). Consultables par l'agent comme référence pendant le développement.

---

## Problèmes transversaux identifiés

### Maintenance des fichiers de navigation
`__summary.md` se désynchronise dès qu'on modifie l'arborescence. Aucun mécanisme automatique aujourd'hui pour le régénérer. Question ouverte : script de génération, convention manuelle stricte, ou autre.

### Pas de séparation claire usage / contribution
Le knowledge mélange ce qui est utile pour *utiliser* l'outil et ce qui est utile pour *le modifier*. La contribution concerne aussi bien les humains que les agents IA (c'est un objectif principal).

### `AGENTS.md` et `CLAUDE.md` sous-exploités
Ces fichiers existent à la racine mais sont vides. Ils pourraient/devraient être générés par le même système que les README, avec des fragments provenant de différents niveaux (projet, suite).

### Pas de standard reproductible
Chaque projet a sa propre variante du système. Le but est de standardiser la convention `.wex/knowledge/` pour qu'elle soit applicable partout, avec un minimum de friction.

### Duplication vs. source unique
Le principe DRY est posé (une seule source de vérité, le reste importé/scripté), mais pas systématiquement appliqué. Certains contenus sont encore dupliqués ou maintenus manuellement.

---

## Principes déjà posés

- **DRY** : ne pas répéter une affirmation, scripter la production de contenu.
- **Génération par templates** : système filestate (Jinja-like) pour produire README et potentiellement d'autres fichiers.
- **Injection multi-niveaux** : contenu projet + contenu suite parente + contenu générique.
- **Roadmap comme outil de collaboration** : fichiers de phases avec cases à cocher, `todo/` actif / `done/` archivé.
- **`__entrypoint.md`** : rendre les agents autonomes dans la navigation du knowledge.
- **Décisions tracées** : pattern ADR pour consigner les choix flous et les trancher explicitement.
- **Les agents contribuent** : la documentation doit être lisible et modifiable par des agents, pas seulement par des humains.
