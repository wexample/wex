# environment-variables.md : passages contradictoires (renommage mixin, roadmap @require_local_env)

Opened: 2026-08-20
Updated: 2026-08-20
Author: agent:spelling

Fichier : `.wex/knowledge/usage/environment-variables.md`

Deux passages se contredisent avec le reste du document (repéré lors d'une passe orthographe, non corrigé — hors domaine) :

1. **Ligne 97** — « **Naming trompeur** : … À renommer (`WithSetupEnvParameterMixin`, cf. roadmap). » Le mixin s'appelle **déjà** `WithSetupEnvParameterMixin` partout dans le doc (lignes 21, 34, 87, 182, 523). Le nom cible et le nom actuel sont identiques : soit le renommage est fait et la note doit sauter, soit le nom cible indiqué est faux.

2. **Ligne 535** — « Solution prévue : décorateur `@require_local_env` (roadmap), bloqué tant que le ménage des fichiers n'est pas fait. » La section 9 (lignes 350-417) documente `@require_local_env` comme **existant**, avec API, exemples réels (`app::release__publish`) et usage direct via `check_env_requirements`. L'entrée « État des lieux » est à mettre à jour.

Accessoire : `PIPY_TOKEN` (lignes 376, 390) vs « token PyPI » (ligne 103) — à vérifier si l'identifiant réel dans le code est bien `PIPY_TOKEN` (faute figée côté code) ou `PYPI_TOKEN`. Non touché : identifiant, pas de la prose.
