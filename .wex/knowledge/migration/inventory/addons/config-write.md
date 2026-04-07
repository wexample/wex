Ce qui est bien
Le pipeline QueuedCollectionResponse est propre — les étapes sont lisibles, ordonnées, séparables.
La séparation runtime.yml / docker.env / docker-compose.runtime.yml est logique.
AppService comme objet plutôt que str — bon choix.
service.yml + docker.compose déclaratif — bien.
Ce qui est mauvais
1. _services_runtime est un hack
   Importer des fichiers Python avec importlib.util.spec_from_file_location pour appeler une fonction décorée — ça bypass tout le système de kernel, les middlewares, les resolvers. C'est fragile et incohérent avec le reste.

2. Le runtime config est réécrit N fois
   Chaque service appelle build_runtime_config_value().to_dict() + dict_merge + rewrite. Si l'ordre des services change ou si deux services écrivent la même clé, résultat imprévisible.

3. _env connaît trop de choses
   Il sait comment nommer les variables de chaque service, comment lire bind, service.*.name, service.*.port... C'est du couplage fort. Si on ajoute un nouveau service avec une logique différente, il faut modifier _env.

4. Les services ne sont pas vraiment des participants
   Un service "contribue" au runtime via un fichier Python qu'on importe à la main. Il devrait pouvoir déclarer ce qu'il apporte sans qu'on aille le chercher avec des hacks.

Ce que serait la version world class
Principe : config/write est un orchestrateur pur. Il ne connaît pas les services. Il demande à chaque service "qu'est-ce que tu contribues ?" et merge.


config/write
1. Chaque AppService.get_runtime_contribution() → dict
2. Merge all contributions → runtime.yml (une seule écriture)
3. runtime.yml → docker.env (projection mécanique, pas de logique métier)
4. docker compose config → docker-compose.runtime.yml
   AppService devient riche :


app_service.get_runtime_contribution() -> dict
# → lit service.yml + config.yml + logique propre au service
# → retourne { "bind": {...}, "service.mysql": {...} }
service.yml devient plus déclaratif :


runtime:
bind:
web_php_ini: php/web.{env}.ini   # résolu par AppService
env:
HOST: service.mysql.host
PORT: service.mysql.port
docker.env devient une projection mécanique du runtime.yml via une table de mapping v5→v6, sans logique.

Proposition concrète pour démarrer
Ajouter get_runtime_contribution(app_env) -> dict sur AppService — chaque service sait ce qu'il contribue
config/write._runtime merge toutes les contributions en une passe → une seule écriture du runtime.yml
config/write._env fait une projection mécanique du runtime.yml → plus de logique service dedans
Supprimer _services_runtime