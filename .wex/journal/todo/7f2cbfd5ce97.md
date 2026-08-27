# Rebuild knowledge wex-addon-app après ajout page knowledge-search

Opened: 2026-08-27
Updated: 2026-08-27
Author: agent:main

Un `wex app::state/rectify` lancé en arrière-plan dans `wex-addon-app` pour reconstruire `built/en/` (après ajout de la page `knowledge-search`) a été tué avant la fin. La sortie construite (`built/en/`) n'est donc pas à jour par rapport à cette nouvelle page. Il faut relancer le rectify pour ce package jusqu'à complétion.
