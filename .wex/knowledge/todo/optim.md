# Performance & Quality Tooling Roadmap

## Décisions d'architecture

- Les commandes de performance sont des **commandes wex** (`app::performance/...`), pas des options filestate
- Les workdirs qui supportent le profiling implémentent **`WithProfilingWorkdirMixin`**
- La commande vérifie `isinstance(workdir, WithProfilingWorkdirMixin)` — retourne "not supported" sinon
- L'exécution se fait dans un **container Docker** (ressources fixes, reproductibilité)
- Output JSON unifié cross-language

---

## Outil retenu : pytest-benchmark

Parmi les candidats évalués :

| Outil | Décision | Raison |
|---|---|---|
| **pytest-benchmark** | ✅ retenu | intégré pytest, JSON out, comparaison de runs, CI-friendly |
| asv | plus tard | pertinent pour suivi long terme (phase 3), trop complexe pour phase 1 |
| timeit | non | trop bas niveau, pas de workflow, absorbé par pytest-benchmark |
| perf | non | précision marginale, complexité inutile en phase 1 |

Contraintes d'environnement (CPU pinning, turbo boost) → gérées par le container Docker.

---

## Command lifecycle (cross-language)

### Tests & coverage
| Commande | Rôle | Bloquant |
|---|---|---|
| `app::test/run` | Lance la suite de tests (pytest, phpunit, jest, flutter test…) | oui (CI) |
| `app::test/coverage` | Tests + rapport de coverage | non |
| `app::test/watch` | Tests en mode watch (dev local) | — |

### Qualité statique
| Commande | Rôle | Bloquant |
|---|---|---|
| `app::lint/run` | Lint (flake8, phpcs, eslint, dart analyze…) | oui (CI) |
| `app::lint/fix` | Correction automatique (black, phpcbf, eslint --fix…) | — |
| `app::rectify/run` | Rectifications structurelles custom (pipeline existant) | optionnel |

### Performance
| Commande | Rôle | Bloquant |
|---|---|---|
| `app::performance/report` | Lance pytest-benchmark, retourne JSON structuré. Python uniquement phase 1. | non |
| `app::performance/baseline` | Sauvegarde le JSON courant comme baseline | — |
| `app::performance/compare` | Diff vs baseline, affiche les régressions | optionnel (CI) |

### Sécurité
| Commande | Rôle | Bloquant |
|---|---|---|
| `app::security/audit` | Audit dépendances (pip-audit, composer audit, npm audit…) | optionnel (CI) |

---

## Roadmap

### Phase 1 — rapport Python pur
- [ ] `WithProfilingWorkdirMixin` dans `wex-addon-dev-python`
  - méthode `run_profiling()` → JSON `{ tool, language, entries: [{ name, p50_ms, p95_ms, memory_mb }] }`
  - utilise `DockerRunner` avec image Python + pytest-benchmark
- [ ] `PythonWorkdir` hérite de `WithProfilingWorkdirMixin`
- [ ] Dockerfile `python-profiling` (Python 3.12 + pytest + pytest-benchmark)
- [ ] Commande `app::performance/report`
  - récupère le workdir courant
  - `isinstance(workdir, WithProfilingWorkdirMixin)` → sinon "not supported"
  - appelle `run_profiling()` et retourne le résultat

### Phase 2 — baseline & comparaison
- [ ] Stockage baseline : fichier `.wex/performance/baseline.json` versionné
- [ ] `app::performance/baseline`
- [ ] `app::performance/compare` — diff % par entrée, affiche régressions
- [ ] Intégration optionnelle dans `bin/publish` (`--no-perf`)

### Phase 3 — CI bloquant + autres langages
- [ ] Seuil de régression configurable (ex: +20% p95 = fail)
- [ ] `app::performance/compare` bloquant en CI
- [ ] `WithProfilingWorkdirMixin` pour PHP (Blackfire/phpbench)
- [ ] `WithProfilingWorkdirMixin` pour JavaScript (clinic.js)
- [ ] Évaluer asv pour suivi historique long terme

### Phase 4 — rectification automatique
- [ ] Patterns lents connus → `app::performance/rectify`
- [ ] Intégration pipeline rectify existant
