# CommandMethodWrapper : champ extra:dict pour config_requirements app

Opened: 2026-08-27
Updated: 2026-08-27
Author: agent:main

Design accepté en fin d'échange mais implémentation non confirmée dans la conversation — à vérifier/terminer.

Contexte : `config_requirements` (vérification qu'une commande app dispose bien de sa config) est un concept propre à l'addon app, pas à core. Deux tentatives rejetées avant d'arriver au bon compromis :
1. Champ `config_requirements: list[dict]` directement sur `CommandMethodWrapper` (dans core) → rejeté : "Sauf que config_requirements est un concept APP que tu viens de fourrer dans CORE !"
2. Stocker `_config_requirements` comme attribut arbitraire sur l'objet fonction Python → rejeté comme "un peu moche".

Compromis retenu : core expose un champ générique opaque `extra: dict` sur `CommandMethodWrapper` (storage clé/valeur neutre, sans sémantique), et l'addon app y range sa propre clé `"config_requirements"`. `require_app_config` doit appender dans ce dict plutôt que d'écrire sur `.function` ou de créer un champ dédié dans core. `AppMiddleware` continue de lire/vérifier ces requirements après injection de `app_workdir` (logique extraite dans `check_config_requirements()`).

À faire : vérifier que ce champ `extra: dict` a bien été ajouté à `CommandMethodWrapper` et que `require_app_config`/`AppMiddleware` l'utilisent ; sinon l'implémenter.
