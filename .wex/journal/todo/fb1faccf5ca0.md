# DiskPersistedRegistry : exigence anti-désynchronisation du cache

Opened: 2026-08-28
Updated: 2026-08-28
Author: agent:main

Complète le todo `e3a174b669f8` (registrification : KernelRegistry → DiskPersistedRegistry).

Avant/pendant l'implémentation de `DiskPersistedRegistry` (registre in-memory adossé à un fichier disque via `StructuredFile`), l'opérateur a posé une question restée sans réponse dans la conversation :

> J'ai une question sur le cache, je suis d'accord que c'est souvent l'option magique. Mais j'ai pas envie de mettre en place un truc qui me ferai perdre 40 minutes demain parce qu'on a oublié qu'il était là et qu'il s'est désynchronisé tu vois. Si on mets en place [le cache], je veux que ce soit nickel et transparent dès le départ. Tu penses que ça peut nous jouer des tours ?

À traiter avant de finaliser le design : identifier explicitement les risques de désynchronisation entre le cache mémoire du registre et le fichier disque (écritures concurrentes, process externe modifiant le fichier, invalidation manquante), et s'assurer que le mécanisme est soit garanti cohérent, soit qu'il expose clairement ses limites — pas une désynchronisation silencieuse à découvrir plus tard.
