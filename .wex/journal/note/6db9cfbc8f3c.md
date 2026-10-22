# Préférence : tri déterministe par path

Written: 2026-08-27
Author: agent:main

Face à un choix d'ordre pour `result.operations` (options: A non-déterministe, B sort by path, C sort by DFS), la préférence exprimée est de trier par path plutôt que par nom : « j'aime bien les trucs triés... j'ai tendance a trier mes variables par nom.... par path alors ? ».

Décision retenue et appliquée pour ce cas précis : sort by path (déterministe, comparable run-à-run), avec les logs différés et replayés dans cet ordre trié.

À retenir comme préférence générale pour de futurs choix similaires : en cas de doute sur l'ordre d'une collection sans impact fonctionnel, privilégier un tri déterministe (par path si applicable) plutôt qu'un ordre non-déterministe ou d'insertion.
