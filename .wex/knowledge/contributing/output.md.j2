# Output — prompts vs logs vs responses

## Three distinct concerns

| | Prompt | Log | Response |
|---|---|---|---|
| **Destinataire** | Humain au terminal | Système / ops | Consommateur de data |
| **Mécanisme** | `context.io.*` (wexample-prompt) | `kernel.logger` (Python logging) | Types de réponse (`DictResponse`, …) |
| **Destination** | stdout / tty | stderr / fichier / aggregator | stdout (format `str` ou `json`) |
| **Silençable** | Oui (`--quiet`, `output_target=none`) | Non (survit au `--quiet`) | Oui (`output_target=none`) |

## Règle de décision

> *"Si un ops ou un script a besoin de le lire, c'est un log. Si c'est pour un humain en train de taper, c'est un prompt."*

## Cas container / service

Quand wex tourne dans un container Docker ou en service systemd :
- Les **prompts** peuvent être silencés — c'est voulu, personne ne les lit
- Les **logs** sont toujours capturés (`docker logs`, journald, etc.) — c'est pour ça qu'ils existent
- Les **responses** en `json` sont exploitables par les scripts qui appellent wex

## Exemples

```python
# ✅ Prompt — destiné à l'humain
context.io.log("Building registry...")
context.io.success("Done.")

# ✅ Log — destiné au système
kernel.logger.info("Registry hydrated in 0.3s")
kernel.logger.warning("Service config not found, using defaults")
kernel.logger.debug("Resolver chain: addon → service → user")

# ❌ Ne pas utiliser logger pour du feedback utilisateur
kernel.logger.info("Starting app...")  # silencieux en prod, l'humain ne le verra pas

# ❌ Ne pas utiliser io pour du diagnostic technique
context.io.log(f"Registry keys: {list(registry.keys())}")  # bruit pour l'humain
```

## Niveaux de log selon verbosity

| Flag | `VerbosityLevel` | `logging` level |
|---|---|---|
| `--quiet` | QUIET | CRITICAL |
| _(défaut)_ | DEFAULT | WARNING |
| `--v` | MEDIUM | INFO |
| `--vv` | HIGH | INFO |
| `--vvv` | MAXIMUM | DEBUG |
