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

# Method API

- ```bash``` : This folder contain all bash scripts
- ```bash/ubuntu1-16.x``` and ```bash/wexample``` : Are the two scripts namespaces. ```bash/wexample``` is loaded only in a wexample site root directory.
- Each folder contain she script group, ex : ```bash/default/file``` folder contains all ```wex file/...``` scripts (or ```wex default::file/...```)
- Each .sh file in these folders are the script name, ex : ```bash/default/file/exists.sh``` allow to execute ```wex file/exists```
- Script function is named like that : ```fileExists() { ...```
- Function arguments are passed into : ```fileExistsArgs() { ```, see file for array structure convention.
- The arguments structure : ```argument_name a "Description" false```
  > argument_name will be accessed into function as ${ARGUMENT_NAME}.
  > 'a' is an alias of argument for shorten calls.
  > Description will be used in help response and when argument is required.
  > true/false mean required or not, if required but not present, prompt user using description content.
- This is the full example

```bash
#!/usr/bin/env bash

fileExistsArgs() {
  _ARGUMENTS=(
    # argument a "Description" true/false (required)
    [0]='file f "File" true'
  )
}

fileExists() {
  [[ -f ${FILE} ]] && echo true || echo false
}

```

Every function can display help for argument usage when using ```--help``` argument ```wex file/exists --help```.

# Wexample sites management

## Docker "services"

Each service is composed by parts of docker-compose.yml, which are mixed together when installed on website.

They contains sample data which can be modified, and base files which is useful to inherit, in order to keep only project specific configuration.

When a site is started, there is the default behavior of common services :

    mysite/docker/docker-compose.local.yml
    T > Contains environment specific configuration (ex: clear passwords)
    | * Mixed with
    |
    v
    site/docker/docker-compose.yml
    T > Contains common editable configuration
    | * Services extends
    |
    v
    (wex)docker/services/[service_name]/docker-compose.local.yml
    T > Contains default environment specific configuration
    | * Services extends
    |
    v
    (wex)docker/services/[service_name]/docker-compose.yml
      > Contains default configuration
  
The final running docker compose yml file is stored into ```./tmp/docker-compose.build.yml``` when running ```wex config/write```.


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
- **PROD_SSH_HOST** : Production server IP.
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

#### Install mail server
  
- Create a new site using service mailserver
- Register at least one mail account
- Go into the site and execute `wex mail/dkim` to generate a 1024 TXT DNS entry
- Edit your DNS Zone by
  * Adding a A mail domain like mail.wexample.com or a CNAME as an alias of an existing domain
  * Create two MX records pointing to mail.wexample.com
    - First with priority 0
    - Second with priority 10
  * Create a TXT entry using DKIM content generated in [mailserver]/config/opendkim/keys/wexample.com/mail.txt
  * Create a TXT record with "v=spf1 ip4:123.123.123.123 ~all" with the server IP
- Wait too long, around 24h
- Start mail server
- Create at least on mail : wex mail/command -g=mail -a=add -d="postmaster@domain.com"
- Restart mail server 