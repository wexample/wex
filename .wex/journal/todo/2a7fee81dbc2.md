# Renommage pdf_generator → syrtis_pdf_generator incomplet (occurrences restantes)

Opened: 2026-08-27
Updated: 2026-08-27
Author: agent:main

Le renommage du package SYRTIS `pdf_generator` en `syrtis_pdf_generator` est incomplet — voir la note déjà filée `1a7b5b70195c` (import obsolète dans `http_server.py`, déjà corrigé).

En testant le daemon HTTP du service (`wex app::container/list` puis vérification que le serveur répond sur 0.0.0.0:8000), deux autres occurrences de l'ancien nom `pdf_generator` ont été repérées et restent à corriger dans le repo SYRTIS :

1. `project/utilities/pdf-generator/src/syrtis_pdf_generator/__main__.py:30` — `from pdf_generator.engine.document import Document`
2. `project/utilities/pdf-generator/generate_demos.yml:14` — `python -m pdf_generator generate`

À corriger puis relancer `wex app/restart --rebuild`.
