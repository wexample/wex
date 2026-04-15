# Roadmap : async

À faire en une seule passe (cohérence step ↔ commande).

## A1 — Step `sync: false` (Y4)

Dans `BashScriptRunner.run()` et `DockerScriptRunner.run()` :
`subprocess.Popen(cmd, start_new_session=True)` sans `.wait()`, retourne `None`.

Ajouter `"sync"` à `get_step_options()` sur ces deux runners.

```yaml
- script: start_service.sh
  sync: false
```

## A2 — Décorateur `async` au niveau commande

Questions à trancher avant d'implémenter :
- Comportement : détaché (fire & forget) ou loggué quelque part ?
- Scope : toujours async quelle que soit la façon d'appeler (direct, attach, step) ?

Implémentation probable :
- `async_command: bool` dans `CommandMethodWrapper`
- `{name: async}` reconnu dans `YamlCommandDefinition._parse_decorators`
- Au dispatch : `subprocess.Popen(["wex", request.name, ...args...], start_new_session=True)`
- Pour Python : même mécanique via le nom de commande résolu

```yaml
decorators:
  - name: async
scripts:
  - script: long_running_job.sh
```
