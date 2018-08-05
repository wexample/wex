[![build status](http://gitlab.wexample.com/wexample-public/scripts/badges/master/build.svg)](http://gitlab.wexample.com/wexample-public/scripts/commits/master)

Automates what others doesn't.

![Scripts]
(cover.jpg)

# Requirements

- Bash
- Git
- Docker

# Install

- Clone the repository into /opt/wexample
  > `git clone https://github.com/wexample/scripts.git /opt/wexample`
- Execute `bash /opt/wexample/install.sh`
- Check install with `wex hi`

# Update

- `wex wex/update`

# Writing a script

For example, you want to add this command :
 
    wex foo/bar --arg=yes --arg2=true

Shortened as :

    wex foo/bar -a=yes -a2

This script will be accessible in all contexts. So create a ne `.sh` file at this path :

    project/bash/default/foo/bar.sh
    
And there is the content of your script file :

```bash
#!/usr/bin/env bash

fooBarArgs() {
  _ARGUMENTS=(
    # argument a "Description" true/false (required)
    [0]='arg a "First argument" true'
    [1]='arg2 a2 "Second argument (boolean)" false'
  )
}

fooBar() {
  echo "First arg "${ARG}
  echo "Second arg "${ARG2}
}

```

## Notes
  > Description will be used in help response and when argument is required.
  > true/false mean required or not, if required but not present, prompt user using description content.
  > Every function can display help for argument usage when using `--help` argument `wex foo/bar --help`.

# Wexample sites management

Wex websites uses specific files structure in order to be ran and deployed with ease.

## Creating a new site

- Go to your website root folder
- Run `wex site/init -s=serviceName,serviceNameTwo`
- It will use the current folder name as project name

## Installing an existing site

After cloning the site form the git repo, just go into site root and run

    wex site/install

This will execute install script depending to the services used. It also execute custom scripts placed into the `ci/install.sh` file if present. 

## Running a wex site

   wex site/start

## Running issues

If your website does not run properly there is some tips :
   
```bash
# Check if all containers are running
docker logs -a
```

If you want to reload Docker IP host binding or other services fast refresh tools (like apache reload for web container)

    wex site/refresh

## .wex

If present, the scripts execution uses the wexample namespace before default namespaces, ex :

```bash
# Try to execute wex wexample::site/start if present.
wex site/start
```

## Wex Services

Services are wrapper of docker services and uses most of the time one of them, sometime more than one. You can see the list of available services by using :

    wex wexample::services/list

There are based on Docker images, available on the Docker Hub.

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
    (wex)services/[service_name]/docker-compose.local.yml
    T > Contains default environment specific configuration
    | * Services extends
    |
    v
    (wex)services/[service_name]/docker-compose.yml
      > Contains default configuration
  
The final running docker compose yml file is stored into ```./tmp/docker-compose.build.yml``` when running ```wex config/write```.

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

This is an explanation on how databases dumps transfer works between environments.

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

Thanks
======


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

