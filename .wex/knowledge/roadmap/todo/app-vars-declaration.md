# Roadmap : déclaration des vars d'app via `config.yml → vars:`

## Contexte

Doc de référence : `.wex/knowledge/usage/environment-variables.md`, section 8.

Après inspection de 5 apps réelles (test, bdo-letters, api, core, manager),
on a identifié **4 catégories de vars d'env** :

| Cat. | Exemples | État | Mécanisme |
|---|---|---|---|
| A. Built-ins runtime wex | `APP_PATH`, `APP_DOMAIN`, `SERVICE_*_COMPOSE`, `BIND_*` | ✅ | Injectées par wex |
| B. Vars de service | `SUPABASE_*`, `SERVICE_N8N_BASIC_AUTH_*` | ✅ | `service.yml → vars:` + `service/install` |
| C. **Vars spécifiques app** | `DOCUSIGN_*`, `MANAGER_BASIC_AUTH`, `IMAGE_BRANCH`, `SYRTIS_*_PATH`, `PACKAGE_PUBLICATION_NPM_TOKEN`… | ❌ | **Aucun** — édition manuelle de `.env`/`env.yml` |
| D. Vars de `libraries:` | `${SYRTIS_REACT_UI_PATH}`, `${PDF_GENERATOR_PATH}` (référencées dans `config.yml → libraries:`) | ❌ | **Aucun** — sous-cas de C |

→ La **catégorie C** est le seul vrai trou (15+ vars dans `bdo-letters`).
La catégorie D est un sous-cas à intégrer dans le même flow.

## Principe

Symétrie avec `service.yml → vars:` (mécanisme existant, éprouvé) :
**format YAML déclaratif** dans `config.yml`, prompt+persist dans
`.wex/local/env.yml` au moment du `app::start` (et autres commandes qui en dépendent).

Pas de scanner automatique du docker-compose — trop fragile (faux positifs/négatifs,
variables techniques internes). On déclare explicitement ce dont on a besoin.

## Format cible

```yaml
# .wex/config.yml
vars:
  DOCUSIGN_ACCOUNT_ID:
    required: true
    description: "DocuSign account ID"
  VITE_DOCUSIGN_DEV:
    default: "false"
    description: "Enable DocuSign dev mode"
  PACKAGE_PUBLICATION_NPM_TOKEN:
    required: true
    description: "NPM publication token"
    use_suite_fallback: true
```

Schéma de chaque entrée (aligné sur `service.yml → vars:`) :

| Champ | Type | Rôle |
|---|---|---|
| `required` | bool | Si `true`, prompt à l'utilisateur si absente |
| `default` | str | Si présent, écrit silencieusement (et override `required`) |
| `description` | str | Affiché dans le prompt |
| `generated` | bool | Si `true`, générée par du code (skip prompt) — à voir si utile au niveau app |
| `use_suite_fallback` | bool | Si `true`, accepte la var trouvée au niveau suite parente |

## Phase 1 — Implémentation du check

- [ ] Créer une fonction `check_app_vars_requirements(app_workdir, io)` qui :
  - Lit `config.yml → vars:` du workdir
  - Pour chaque var avec `default` et absente : `set_env_parameters({k: default})`
  - Pour chaque var `required: true` et absente : prompt → persist
  - Si `use_suite_fallback: true` → lookup via `get_env_parameter_or_suite_fallback`
- [ ] Factoriser avec le code déjà présent dans `service/install.py` (la logique
  service_vars est très similaire) — peut-être extraire un helper commun.

## Phase 2 — Hook au démarrage de l'app

- [ ] Brancher `check_app_vars_requirements()` sur `app::start` (et toute commande
  qui ferait `docker compose up` derrière). Option : extension du `AppMiddleware`
  pour lire `command_wrapper.extra` et déclencher si la commande l'a déclaré.
- [ ] Cas concret à valider : sur `bdo-letters`, supprimer manuellement
  `DOCUSIGN_ACCOUNT_ID` de `.wex/local/env.yml` puis lancer `app::start` →
  doit prompter avant de lancer docker.

## Phase 3 — Intégration `libraries:`

Le résolveur de `config.yml → libraries:` accepte des `${VAR}` :

```yaml
libraries:
  - ${SYRTIS_REACT_UI_PATH}
  - ${PDF_GENERATOR_PATH}
```

- [ ] Quand le résolveur trouve un `${VAR}` dans une entrée `libraries:`, vérifier
  que la var est déclarée dans `config.yml → vars:`. Sinon → warning ou erreur.
- [ ] Optionnel : convention « toute `${VAR}` dans `libraries:` est implicitement
  `required` » pour éviter de devoir la redéclarer dans `vars:`. À trancher.

## Phase 4 — Migration des apps existantes

- [ ] Sur les apps réelles (bdo-letters, api, core, manager), produire des
  `config.yml → vars:` à partir du contenu actuel de leur `.env` legacy.
  Possible script d'aide qui diff `compose ${VAR}` vs `local/env.yml` → propose
  une déclaration.
- [ ] Tester le flow complet (suppression d'une var, prompt, persist, restart).

## Phase 5 — Doc

- [ ] Mettre à jour la section 8 de `environment-variables.md` une fois
  l'implémentation faite (la section décrit déjà le mécanisme cible).
- [ ] Ajouter un exemple `vars:` dans un éventuel template de `config.yml`
  généré par `app::app/init`.

---

## Notes

- Pas d'auto-scan du compose : on déclare ce dont on a besoin, on ne devine pas.
- Le mécanisme **réutilise** la persistance YAML existante, pas de stockage parallèle.
- Le prompt arrive **au lancement de la commande** (`app::start`), pas dans le subprocess
  (cf. décisions de la roadmap `require-local-env-decorator.md`).
