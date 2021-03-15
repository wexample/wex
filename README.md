# wex v3.4

A web developer automation tool and deployment system.

## Install

### Ubuntu

- Clone the repository and install
  > `sudo git clone --depth=1 https://github.com/wexample/wex.git /opt/wex && sudo bash /opt/wex/install`
- Check install with `wex hi`

## On MacOS

- Install brew
- Update your bash and install coreutils with `brew install bash coreutils`
- Double check this folders are allowed to be mounted with Docker (Docker manager > Resources > Files Sharing)
  * /opt/wex
  * The folder of the project you want to run
- Then see Ubuntu installation process below
- Run your site in `sudo wex site/start`
- Once the project runs, think to restart your browser

### MacOS notices

- Using port `80`is not allowed for local server so you should access your sites with port `4242`, eg: `http://mysite.wex:4242`

# Usage

## Cheat sheet

This is the most common command used to manage your apps.

```bash
# Clear site cache only.
wex cache/clear
# Execute command for site cli.
wex cli/exec -c="my:command"
# Format source code using available tools
wex code/format
# Make current database anonymous (dev / RGPD).
wex db/anon
# Stops all running docker containers
wex docker/stopAll
# Create a new migration file.
wex migration/create
# Create a new migration file base on code entities changes.
wex migration/diff
# Execute database migrations.
wex migration/migrate
# Edit site entity.
wex entity/edit
# Reset all site assets.
wex site/build
# Install all site packages, dependencies, assets..
wex site/install
# Give all useful permissions.
wex site/perms
# Start current site
wex site/start
# Run unit test for given website
wex site/test -f=project/tests/file.php -m=testMethod
# Update all packages.
wex site/update
# Reload web server.
wex site/serve
# Start watcher.
wex watcher/start
# Import a database dump
Put an SQL file in `mysql/dumps`, then
wex db/restore
```

# Updating

    wex core/update
    
# Uninstalling

Want to get rid of the `wex` commands ? All right.

    wex core/uninstall
    
If you still want to une Docker containers to launch your site, you can still use the docker compose file placed at `yoursite/tmp/docker-compose.build.yml`
    
# Writing a script

## File structure

For example, you want to add this command :
 
    wex foo/bar --arg yes --arg2 true
    wex foo/bar --arg=yes --arg2=true

Shortened as :

    wex foo/bar -a yes -a2
    wex foo/bar -a=yes -a2

This script will be accessible in all contexts. So create a ne `.sh` file at this path :

    project/bash/default/foo/bar.sh
    
And there is the content of your script file :

```bash
#!/usr/bin/env bash

fooBarArgs() {
  # Examples of supported config files
  _ARGUMENTS=(
    # argument a "Description" true/false (required)
    'arg a "First argument" true defaultValue'
    'arg2 a2 "Second argument (boolean)" false defaultValue2'
  )
  _AS_SUDO=false
  _DESCRIPTION="This is my foo bar script"
}

fooBar() {
  echo "First arg "${ARG}
  echo "Second arg "${ARG2}
}

```

### Notes
  > Arguments description will be used in help response and when argument is required.
  > true/false mean required or not, if required but not present, use default if exists, else prompt user using description content.
  > Every function can display help for argument usage when using reserved `--help` argument `wex foo/bar --help`.

## Development rules

### Use [ ] instead of [[ ]]

Conditions written inside `[ ... ]` are more portables. It should always have an equivalent of a `[[ ... ]]` condition.
More info here : https://stackoverflow.com/questions/669452/is-double-square-brackets-preferable-over-single-square-brackets-in-ba

## Compatibility

### MacOS

Tips to write compatible scripts.

- Do not use "readlink", prefer 
- For sed :
  > Use `wex file/regex` in place of `sed -i ... filename`
  > Use -E option instead of -r (BSD format)
- In Docker
  > Unable to run sites without port forwarding (on port 80)
  > Do not mount dir that no exists locally

# Testing

Useful to test changes and core compatibility.

- Running all tests is simple as `wex test`.
- Running a specific test (placed into `project/tests/bash`), is simple as `wex test my/test`, example : `wex test config/comment`

# Understanding core

## Core extension

When a script is not found in the main script, it will ask for an action into the `project/extend` directory.

### project/extend/draft

It contains scripts used in production but waiting to e validated.

### project/extend/local

It contains scripts used locally. Theses script will never be versioned.

### project/extend/v2

It contains the previous version of the script for compatibility reason.
