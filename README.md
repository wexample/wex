# wex v3

A web developer automation tool and deployment system.

# Install

- Clone the repository into `/opt/wex`
  > `sudo git clone https://github.com/wexample/wex.git /opt/wex`
- Execute `sudo bash /opt/wex/install.sh`
- Check install with `wex hi`

## Core extension

When a script is not found in the main script, it will ask for an action into the `project/extend` directory.

### project/extend/draft

It contains scripts used in production but waiting to e validated.

### project/extend/local

It contains scripts used locally. Theses script will never be versioned.

### project/extend/v2

It contains the previous version of the script for compatibility reason.
