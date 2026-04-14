# Service Vars Manifest

> Permettre aux services de déclarer leurs variables d'environnement dans `service.yml`,
> avec prompting interactif lors de l'install pour les vars non générées.

## Contexte

En v5, les vars étaient éparpillées (hardcodées dans install, dans config.yml, etc.).
En v6, chaque service déclare ses vars dans `service.yml` → un seul endroit de vérité.

Le flow cible :
1. `service/install` lit la section `vars:` du `service.yml`
2. Pour chaque var `required: true` sans `generated: true` ni `default:` → prompt interactif
3. Les vars générées (JWT secret, tokens) restent dans `install.py` du service
4. `app/start` peut valider que les vars requises sont présentes avant de démarrer

## Spec `service.yml` — section `vars:`

```yaml
vars:
  SUPABASE_PUBLIC_URL:
    required: true
    description: "Public URL for the Supabase API (e.g. https://api.myapp.com)"
  SUPABASE_JWT_SECRET:
    generated: true          # install.py s'en charge, pas de prompt
    description: "JWT secret auto-generated at install"
  SUPABASE_DASHBOARD_USERNAME:
    default: "admin"
    description: "Supabase Studio login username"
  SUPABASE_DASHBOARD_PASSWORD:
    generated: true
    description: "Dashboard password auto-generated at install"
```

### Attributs

| Attribut      | Type    | Comportement                                               |
|---------------|---------|------------------------------------------------------------|
| `required`    | bool    | Var obligatoire — erreur si absente au démarrage           |
| `generated`   | bool    | Ne pas prompter ; `install.py` gère la génération          |
| `default`     | string  | Valeur pré-remplie, écrite dans `.env` sans prompt         |
| `description` | string  | Affiché lors du prompt ou dans `service/vars/list`         |

### Règles de résolution

- `generated: true` → skip prompt, `install.py` écrit la valeur
- `default: "x"` → écrire `KEY=x` dans `.env` sans prompt (si absent)
- `required: true` sans generated/default → prompt interactif
- Var déjà présente dans `.env` → toujours skip (ne jamais écraser)

---

## Étapes

### Étape 1 — Parser `vars:` dans `ServiceDefinition`

**Fichiers concernés :**
- `wex-addon-app/src/.../service/service_definition.py` (ou équivalent)
- Ajouter une méthode `get_vars() -> dict[str, dict]`

**Critère de succès :** `service_def.get_vars()` retourne le dict tel que défini dans `service.yml`.

---

### Étape 2 — Écriture des `default:` dans `.env` lors de l'install

**Fichiers concernés :**
- `wex-addon-app/src/.../commands/service/install.py`

Après la copie des samples et avant `rectify` :
1. Charger `service_def.get_vars()`
2. Pour chaque var avec `default:` et sans `generated:` → `file_env_append_as_real_user`
3. Skip si la var est déjà présente dans `.env`

**Critère de succès :** `SUPABASE_DASHBOARD_USERNAME=admin` écrit automatiquement.

---

### Étape 3 — Prompt interactif pour les vars `required` sans default/generated

**Fichiers concernés :**
- `wex-addon-app/src/.../commands/service/install.py`

Pour chaque var `required: true` sans `generated` ni `default` :
- Afficher `description` + `KEY=?`
- Lire input utilisateur
- Écrire dans `.env` via `file_env_append_as_real_user`
- Skip si déjà présente

**Critère de succès :** install de supabase demande `SUPABASE_PUBLIC_URL` en interactif.

---

### Étape 4 — Validation au démarrage (`app/start`)

**Fichiers concernés :**
- `wex-addon-app/src/.../commands/app/start.py`

Avant `docker compose up` :
1. Pour chaque service installé, charger `service_def.get_vars()`
2. Charger les vars depuis `.env`
3. Pour chaque var `required: true` absente → erreur explicite avec le nom + description

**Critère de succès :** `app::app/start` échoue proprement si `SUPABASE_PUBLIC_URL` est absent.

---

### Étape 5 — Commande `app::service/vars/list`

**Nouveau fichier :**
- `wex-addon-app/src/.../commands/service/vars/list.py`

Affiche un tableau des vars de chaque service installé :
- Nom de la var
- Statut (set / missing / generated)
- Description

**Critère de succès :** `wex app::service/vars/list` donne une vue claire de l'état des vars.

---

### Étape 6 — Appliquer sur supabase (cas réel)

- Annoter toutes les vars dans `wex-addon-services-platform/.../services/supabase/service.yml`
- Vérifier que l'install ne prompt que `SUPABASE_PUBLIC_URL`
- Vérifier que les vars générées ne sont pas promptées

---

## Statut

- [x] Étape 1 — Parser `vars:` dans `ServiceDefinition`
- [x] Étape 2 — Écriture des `default:` dans `.env`
- [x] Étape 3 — Prompt interactif
- [ ] Étape 4 — Validation au démarrage
- [ ] Étape 5 — Commande `service/vars/list`
- [ ] Étape 6 — Appliquer sur supabase

## Notes

- `generated: true` = indice "ne pas prompter" ; la logique de génération reste dans `install.py`
- Ne jamais écraser une var déjà présente dans `.env`
- Les vars sont toujours écrites dans `.wex/.env` (gitignored), jamais dans `config.yml`
