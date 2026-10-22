# Critères de décision pour Phase 1.5 async (imports addons)

Written: 2026-08-28
Author: agent:main

Complète le todo `6ca96626acb1` (Roadmap async wex : lancer Phase 1.5 imports addons parallèles).

Avant de démarrer la Phase 1.5, l'opérateur a donné le cadre de décision suivant :

> Moi j'ai envie de te faire confiance, je veux surtout le plus robuste / performant, quitte a ajouter des deps ça me dérange pas. La convention _async ça me va aussi.

Et sur la méthode : ne pas choisir une approche technique dans l'abstrait, mais démarrer le travail et trancher dès qu'un cas concret se présente ("Je ne sais pas quoi choisir sans exemple concret dans notre outil. Est-ce qu'on démarre 1.5 et on décide dès qu'on a un cas ?").

Donc pour toute décision technique restant à prendre dans cette phase (choix de lib async, granularité des tâches, etc.) : privilégier robustesse/perf > minimalisme des dépendances, garder la convention de nommage `_async`, et ne pas bloquer sur une décision a priori — la trancher au premier cas concret rencontré.
