# Hosts Registry — roadmap

Remplacer le mode "single-app" de `hosts/update` par un registre centralisé
qui garde la liste de toutes les apps actives, comme le faisait le proxy en v5.

## Registre

- [x] Créer `common/app_registry.py` → `~/.local/share/cli/registry.yml`
- [x] Format : `{ "apps": { "<app_path>": { "domains": [...], "ip": "...", "env": "..." } } }`
- [x] Écrire/mettre à jour l'entrée de l'app courante au `app::app/start`
- [x] Supprimer l'entrée de l'app courante au `app::app/stop`

## hosts/update

- [x] Lire le registre complet
- [x] Régénérer le bloc depuis toutes les entrées du registre
- [x] Appeler `hosts/update` après chaque écriture dans le registre (start/stop)

## Nettoyage

- [x] Au démarrage de `hosts/update`, purger les entrées dont les containers ne tournent plus
- [x] Commande `app::hosts/clean` pour forcer ce nettoyage manuellement

## Migration

- [x] Supprimer le commentaire `# single-app mode` dans `hosts/update`
- [ ] Migration wex `6.0.x` si des fichiers projets sont impactés
