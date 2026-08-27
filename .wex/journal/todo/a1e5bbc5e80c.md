# Erreur "Unknown model 'sonnet'" bloque la génération de description

Opened: 2026-08-27
Updated: 2026-08-27
Author: agent:main

Une opération de génération automatique de description (`GENERATED_DESCRIPTION_OPERATION`) a échoué avec :

```
⚠ Could not generate a description: Unknown model 'sonnet'. Known models: claude:opus-5, claude:sonnet-5, claude:haiku-4-5.. Leaving global.description unset.
```

Quelque part la config référence l'alias `sonnet` au lieu du nom complet `claude:sonnet-5`, ce qui fait échouer silencieusement la génération et laisse `global.description` vide. L'opérateur a explicitement reporté la correction ("Attends non je demande ailleur") sans jamais y revenir dans cette conversation — le mapping est toujours cassé.

À faire : retrouver où ce mapping de modèle est résolu et corriger l'alias `sonnet` → `claude:sonnet-5` (ou équivalent), pour que la génération de description ne se contente plus de laisser le champ vide en cas d'échec silencieux.
