# Progress bar parallèle : pourquoi le handle ne marche pas tel quel

Written: 2026-08-27
Author: agent:main

Lors du diagnostic du spam console pendant `wex app::state/rectify --dry-run` (inspection parallèle de 488 items avec ThreadPoolExecutor), l'idée d'utiliser un handle de `self.io.progress()` partagé entre threads pour centraliser l'affichage a été étudiée et écartée pour deux raisons factuelles, pas juste un choix de design :

1. **`ProgressHandle.update()` n'est pas thread-safe** : aucun lock interne. Plusieurs threads qui appellent `handle.update(current=N)` en concurrence peuvent perdre des updates (race sur le compteur). Il faudrait un `threading.Lock` côté appelant pour le rendre utilisable en parallèle.
2. **Le rendering n'écrit pas en place** : `handle.update()` fait `auto_render=True`, qui appelle `output.print(...)`, qui écrit une **nouvelle ligne** à chaque update (pas de cursor-up + clear). C'est ce qui provoquait le spam massif (une ligne réimprimée à chaque tick de progression), pas un bug de threading.

Conclusion à l'époque : la lib `prompt` n'a pas d'API native pour afficher l'avancement de N tâches parallèles qui terminent dans le désordre — les progress bars existantes supposent un seul thread qui pilote le tempo. La vraie solution propre nécessiterait un contrôle terminal (redraw in place) et un thread d'affichage dédié — piste évoquée mais dont le résultat concret (tentative de screen UI, abandon pour cause de flickering/empilement) a été traité ailleurs dans la conversation.
