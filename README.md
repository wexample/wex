Wexample Scripts
================


                          m
                     .#########.
                 .888888##K#########.
             .68888888888#~~###########.
          .66666688888!|#P~~~|!###########.
          |~~7666666`  |7~!~~|  `#########|
          |~~~~~7|     |/` `\|     |######|
          |+~~~~~|                 |8#####|
          |+~~~~~|                 |888###|
          |++~~~~|                 |8888##|
          |++++~~~~_     _!_     _8888888#|
           +++++~~~~~~~.+++++.666666888888
              +++++~~~~~~~++22666666668
                  +++++~~~~22226666
                      -+~~~2222
                          *
                                              _
                                             | |
      __      _______  ____ _ _ __ ___  _ __ | | ___
      \ \ /\ / / _ \ \/ / _` | '_ ` _ \| '_ \| |/ _ \
       \ V  V /  __/>  < (_| | | | | | | |_) | |  __/
        \_/\_/ \___/_/\_\__,_|_| |_| |_| .__/|_|\___|
         http://network.wexample.com   | |
                                       |_|


[![build status](http://gitlab.wexample.com/wexample-public/scripts/badges/master/build.svg)](http://gitlab.wexample.com/wexample-public/scripts/commits/master)

These scripts are used to automate common tasks.

## Ressources

- **Semantic versioning** : https://semver.org/

# Wexample sites management

## .wex

If présent the scripts execution uses the wexample namespace before default namespaces, ex :

```bash
# Try to execute wex wexample::site/start if present.
wex site/start
```

### Properties

This file contains main site information. It is generated when using ```wex wexample::site/init```

- **NAME** : site name, *required* 
- **AUTHOR** : Author's name,
- **CREATED** : Site init date,
- **SERVICES** : Wex services separated by a comma, ex : web,mysql,phpmyadmin
- **PROD_IPV4** : Production server IP.
- **PROD_PORT** : Production server port,
- **FILES_XXX** : Path of site files

## Specific behaviors

### Git hooks

To initialize Git hooks, you should execute `wex git/initHooks` on your website (it is executed automatically when using `wex wexample::site/init`). Then the **./git** folder will contain a preconfigured list of hooks fired by Git on several actions.

### wex wexample::site/*

#### Deployment

          |              |                       |
    local | <-- pull --- | repo | --- deploy --> | --- pull --> | prod
          | --- push --> |                       |  
 
### wex wexample::db/*

               local                     prod
               mysql                     mysql
              |  ^  ^                   ^  |  ^
              |  |  |                   |  |  |
        dump  |  |  |                   |  |  |
     restore  |  |  |                   |  |  |
              v  |  +------- sync ------+  v  |
             /dumps -------- push -------> /dumps
                    <------- pull --------


#### Examples :

```bash
# Create a dump in production then pull it locally
wex db/dump -e=prod -p
```

### wex wexample::mail/*

Manage a mail server, see https://www.davd.eu/byecloud-building-a-mailserver-with-modern-webmail/
