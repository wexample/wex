# wex v3

A web developer automation tool and deployment system.

# Install

## On Ubuntu

- Clone the repository into `/opt/wex`
  > `sudo git clone https://github.com/wexample/wex.git /opt/wex`
- Execute `sudo bash /opt/wex/install`
- Check install with `wex hi`

## On MacOS

- Install XCode
- Install brew
- Update your bash and coreutils with `brew install bash coreutils`
- Then see Ubuntu installation process below

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
# Run unit test for given website
wex site/test -f=project/tests/file.php -m=testMethod
# Update all packages.
wex site/update
# Reload web server.
wex site/serve
# Start watcher.
wex watcher/start
```

# Writing scripts



## MacOS compatibility

Tips to write compatible scripts.

- Do not use "readlink", prefer 
- For sed :
  > Use `wex file/regex` in place of `sed -i ... filename`
  > Use -E option instead of -r (BSD format)


# Understanding core

## Core extension

When a script is not found in the main script, it will ask for an action into the `project/extend` directory.

### project/extend/draft

It contains scripts used in production but waiting to e validated.

### project/extend/local

It contains scripts used locally. Theses script will never be versioned.

### project/extend/v2

It contains the previous version of the script for compatibility reason.