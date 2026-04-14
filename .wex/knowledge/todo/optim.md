# Performance & Quality Tooling Roadmap

## Command lifecycle (cross-language)

Commandes universelles qui s'appliquent quel que soit le langage du projet courant.
Chaque commande délègue à l'implémentation spécifique du langage détecté.

### Tests & coverage
| Commande | Rôle | Bloquant |
|---|---|---|
| `app::test/run` | Lance la suite de tests du projet (unittest, pytest, phpunit, jest, flutter test…) | oui (CI) |
| `app::test/coverage` | Lance les tests avec rapport de coverage | non |
| `app::test/watch` | Lance les tests en mode watch (dev local) | — |

### Qualité statique
| Commande | Rôle | Bloquant |
|---|---|---|
| `app::lint/run` | Lint du code (flake8, phpcs, eslint, dart analyze…) | oui (CI) |
| `app::lint/fix` | Correction automatique (black, phpcbf, eslint --fix…) | — |
| `app::rectify/run` | Rectifications structurelles custom (pipeline existant) | optionnel |

### Performance — rapport
| Commande | Rôle | Bloquant |
|---|---|---|
| `app::performance/report` | Profiling + rapport humain (cProfile, Blackfire, clinic.js…). Pas de baseline requise. | non |
| `app::performance/benchmark` | Exécute les benchmarks définis et produit des métriques (p50/p95/mémoire). Tourne dans un container Docker pour isolation. | non |
| `app::performance/baseline` | Sauvegarde les métriques courantes comme baseline de référence | — |
| `app::performance/compare` | Compare les métriques courantes vs la baseline. Affiche les régressions. | optionnel (CI) |

### Performance — optimisation automatique
| Commande | Rôle | Bloquant |
|---|---|---|
| `app::performance/rectify` | Applique les transformations automatiques connues (patterns lents → patterns rapides). S'appuie sur le pipeline rectify existant. | — |

### Sécurité
| Commande | Rôle | Bloquant |
|---|---|---|
| `app::security/audit` | Audit des dépendances (pip-audit, composer audit, npm audit…) | optionnel (CI) |

---

## Roadmap

### Phase 1 — Rapport pur (pas de baseline, pas de blocage)
Objectif : valider l'utilité réelle avant de construire l'infrastructure.

- [ ] Définir le format de sortie JSON unifié cross-language
  ```json
  {
    "language": "python",
    "tool": "cProfile",
    "entries": [
      { "name": "fn_name", "p50_ms": 12.3, "p95_ms": 45.6, "memory_mb": 23.4 }
    ]
  }
  ```
- [ ] `app::performance/report` — Python (cProfile / py-spy)
- [ ] `app::performance/report` — PHP (Blackfire / Xdebug)
- [ ] `app::performance/report` — JavaScript (clinic.js / 0x)
- [ ] `app::test/run` cross-language (détection auto du runner)
- [ ] `app::test/coverage` cross-language

### Phase 2 — Baseline & comparaison
Prérequis de tout blocage CI. Sans baseline, les métriques absolues ne veulent rien dire.

- [ ] Stockage de baseline (fichier JSON versionné dans le repo, par environnement)
- [ ] `app::performance/baseline` — enregistre la baseline courante
- [ ] `app::performance/compare` — diff vs baseline, affiche les régressions en %
- [ ] Intégration dans `bin/publish` (optionnelle, `--no-perf` pour skip)

### Phase 3 — Blocage sur régression (CI)
- [ ] Seuil de régression configurable (ex: +20% sur p95 = fail)
- [ ] `app::performance/compare` devient bloquant en CI
- [ ] `app::security/audit` bloquant en CI

### Phase 4 — Rectification automatique
Seulement pour les patterns 100% déterministes et sans ambiguïté.

- [ ] Identifier les patterns lents documentés par langage
- [ ] `app::performance/rectify` — Python (ex: list comprehension vs map, slot classes…)
- [ ] `app::performance/rectify` — PHP
- [ ] `app::performance/rectify` — JavaScript
- [ ] Intégration dans le pipeline rectify existant

---

## Notes d'implémentation

- Les benchmarks tournent dans un **container Docker à ressources fixes** pour éliminer la variance d'environnement (même approche que les commandes rectify existantes)
- Le format de sortie JSON est identique quel que soit le langage — les commandes de comparaison sont language-agnostiques
- Les commandes `app::` détectent le langage via le workdir existant (filestate)
- Chaque phase est indépendante — ne pas sauter à la phase 4 sans avoir validé la phase 1 sur des cas réels
