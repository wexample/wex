# Roadmap : Réorganisation de la documentation

Mission : nettoyer, mettre à jour et structurer toute la documentation du projet `wex` (et établir un standard réutilisable pour les projets similaires).

---

## Objectifs

1. **Supprimer le contenu mort** — fichiers obsolètes, sections qui ne correspondent plus au code.
2. **Mettre à jour le contenu qui a évolué** — architecture, commandes, concepts renommés.
3. **Ajouter les sections manquantes** — parties du projet non documentées.
4. **Définir une organisation claire des fichiers** — convention applicable à `wex` et à tous les projets du même écosystème.
5. **Structurer pour trois types de lecteurs** :
   - **Humains** — lecture et écriture (clarté, navigation, prose)
   - **Agents IA** — lecture et écriture (entrypoints, summaries, contexte machine-friendly)
   - **Scripts** — lecture et production via templates Jinja, injection de contenu depuis des suites de packages ou environnements externes

---

## Phase 1 — Audit de l'existant

- [ ] Lire tous les fichiers de `.wex/knowledge/` et identifier le contenu mort
- [ ] Identifier les fichiers dont le contenu a évolué (architecture, nommage, concepts)
- [ ] Lister les sections absentes (ce qui existe dans le code mais pas dans la doc)
- [ ] Produire un rapport d'audit (liste : à supprimer / à mettre à jour / à créer)

---

## Phase 2 — Définir la convention d'organisation

- [ ] Décider de l'arborescence cible pour `.wex/knowledge/` (applicable à tous les projets)
- [ ] Définir les fichiers réservés et leur rôle :
  - `__entrypoint.md` — point d'entrée pour les agents IA
  - `__summary.md` / `_summary.md` — index lisible humain et machine par dossier
  - `README.md` — documentation humaine de surface
- [ ] Décider du format des templates Jinja pour la génération scriptée
- [ ] Documenter la convention dans un fichier de référence

---

## Phase 3 — Nettoyage

- [ ] Supprimer les fichiers identifiés comme morts en phase 1
- [ ] Archiver ou déplacer le contenu `migration/done/` si plus pertinent
- [ ] Évaluer si `migration/` reste utile une fois la migration terminée

---

## Phase 4 — Mise à jour du contenu existant

- [ ] Mettre à jour `project/architecture.md` (refléter l'état réel du code)
- [ ] Mettre à jour `coding/` (conventions Python à jour)
- [ ] Mettre à jour `project/dot-wex-directory.md` (structure `.wex/` actuelle)
- [ ] Relire et corriger `readme/` (introduction, testing, webhooks)
- [ ] Mettre à jour les `__summary.md` de chaque dossier

---

## Phase 5 — Ajout des sections manquantes

- [ ] Documenter le système d'addons (découverte, chargement, cycle de vie)
- [ ] Documenter le système de commandes (naming, décorateurs, résolution)
- [ ] Documenter le système filestate (options, opérations, templates)
- [ ] Documenter les runners et la gestion des environnements
- [ ] Documenter l'injection depuis des suites de packages externes

---

## Phase 6 — Outillage pour les scripts et agents

- [ ] Définir les templates Jinja standards pour la génération de fichiers doc
- [ ] Décider du mécanisme d'injection (variables, contexte, sources externes)
- [ ] Créer un exemple de template fonctionnel
- [ ] S'assurer que chaque dossier a un `__summary.md` à jour (lisible par les agents)

---

## Phase 7 — Standardisation multi-projets

- [ ] Extraire la convention d'organisation en document partageable
- [ ] Vérifier l'applicabilité sur les autres projets de l'écosystème (`syrtis`, packages Python/PHP/JS)
- [ ] Éventuellement créer un template de base `.wex/knowledge/` réutilisable
