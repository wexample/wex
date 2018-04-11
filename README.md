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

## wex.json

- **name** : site name, *required* 
- **author** : Author's name,
- **created** : Site init date,
- **services** : Wex services separated by a comma, ex : web,mysql,phpmyadmin
- **prod.ipv4** : Production server IP.
- **prod.port** : Production server port,
- **files.xxx** : Path of site files

## Specific behaviors

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
