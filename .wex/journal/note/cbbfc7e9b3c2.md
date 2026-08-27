# Nettoyage knowledge Python — état final

Written: 2026-08-27
Author: agent:main

Purge et rangement des fichiers `.wex/knowledge/` (et vestiges `.wex/doc/` v5) sur l'ensemble des packages Python du dépôt, décidé et exécuté en une passe fin 2026 :

**Supprimés (7 fichiers)** :
- `filestate/.wex/doc/{_entrypoint,_summary}.md` et `doc/project-info/_summary.md` — vestiges v5
- `event/knowledge/dev/roadmap.md` — plan en 5 points intégralement réalisé (`Event`, `dispatcher`, `listener`, `priority`, `dispatch_event_async`, `EventPriority`)
- `prompt/knowledge/{changelog,migration}/0.0.22.md` — le paquet est en 14.1.0, plus aucun lecteur possible
- `filestate/.wex/doc/project-info/project-conventions.md`

**Déplacés vers l'emplacement conventionnel** :
- `api`: `knowledge/dev/rework.md` → `journal/todo/abstract-gateway-rework.md` (renommé)
- `helpers`, `wex-addon-ai`: tickets `knowledge/todo/` → `journal/todo/`
- `wex-core`: `features/app-level-command.md` → `usage/`
- `filestate`: 6 fragments de `.wex/doc/readme/` répartis en `usage/{concepts,configuration,features,options}.md` et `contributing/{operations,option-testing}.md` ; `.wex/doc` n'existe plus
- `prompt`: `package.md` scindé (usage de l'IoManager vs marche à suivre pour ajouter un type de réponse)

Résultat : 21 fichiers de knowledge sous Python, tous à leur place (`usage/`, `contributing/`, `specifications/`). Le même passage n'a pas été refait pour les autres langages (PHP, JS) dans ce lot — décision de l'opérateur : « rien n'est hors scope, il faut tout faire, dans un ordre ou dans un autre », donc à reprendre ailleurs si du pollution similaire y est repérée.
