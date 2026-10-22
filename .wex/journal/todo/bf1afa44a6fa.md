# Runner YAML python : le scope des variables n'est jamais alimenté

Opened: 2026-08-27
Updated: 2026-08-27
Author: agent:main

## Le fait, vérifié dans le code

`PythonScriptResponse.scope` (wex-core, `yaml/python_script_response.py`) se décrit ainsi :

```python
scope: dict = public_field(
    factory=dict,
    description="Variables injected into the script's local scope (kernel, env vars, options)",
)
```

Son unique appelant, `PythonScriptRunner.run()` (`yaml/runners/python_script_runner.py`), passe :

```python
scope={"kernel": kernel}
```

Les variables ne sont donc jamais injectées. Le chemin prévu existe et n'est pas branché.

## Conséquence

Faute de ce chemin, le seul moyen d'atteindre une variable depuis un step `runner: python`
est la substitution textuelle : `yaml_substitute_step` (`yaml/yaml_variable.py`) remplace
`${VAR}` dans **toutes** les chaînes du step, `script` compris, et le résultat part dans
`exec(self.code, {}, self.scope.copy())`.

C'est ce que la doc de wex-core doit documenter comme un piège
(`.wex/knowledge/built/en/usage/app-level-command.md`, § « Variable substitution ») :
« do NOT use os.environ.get("MY_TOKEN") — not injected into the process ».

Vérifié en exécution — une valeur contenant une apostrophe produit du code exécutable :

```
valeur   : ab"; import os; print(os.getcwd()); x="
généré   : token = "ab"; import os; print(os.getcwd()); x=""
```

Sources des variables (`runner/core_yaml_command_runner.py:36-49`), par priorité croissante :
`.wex/local/env.yml`, **tout `os.environ`**, les options d'invocation, et la sortie capturée
d'un step précédent via la clé `variable:` (`_capture_variable`, ligne 53).
Le runner `bash` suit le même trajet.

## Gravité — ce qui est établi et ce qui ne l'est pas

- **Établi** : bug de robustesse réel. Toute valeur contenant une apostrophe, un guillemet
  ou un saut de ligne corrompt silencieusement le script généré.
- **Non établi** : qu'une entrée non fiable atteigne ces variables aujourd'hui. Le webhook
  (`webhook/handler.py:193`) construit son `subprocess.Popen` en liste d'argv, sans shell,
  et le `command_str` vient de la route configurée — pas des paramètres de requête.
  Je n'ai pas tracé si `--webhook-path` redescend en option d'une commande YAML.

Donc : bug de correction avéré, forme d'injection avérée, vulnérabilité exploitable **non
démontrée**. Elle le deviendrait si un step capturait de la donnée externe (`git log`,
réponse HTTP, nom de fichier) dans une variable réinjectée ensuite dans un `script`.

## Correctif proposé (non appliqué)

Une ligne dans `PythonScriptRunner.run()`, avec un choix de design à trancher :

- `scope={"kernel": kernel, **variables}` — chaque variable devient un nom nu ; expose tout
  `os.environ` en majuscules dans le scope, avec risque de masquage.
- `scope={"kernel": kernel, "variables": variables}` — `variables["MY_TOKEN"]`, plus verbeux,
  sans collision.

Les deux laissent `${VAR}` fonctionner : rien ne casse pour l'existant. À faire ensuite,
si le correctif passe : mettre à jour le § « Variable substitution » de la page de doc, qui
enseigne aujourd'hui le contournement.
