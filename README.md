# wex v3

A web developer automation tool and deployment system.

# Install on Ubuntu

- Clone the repository into `/opt/wex`
  > `sudo git clone https://github.com/wexample/wex.git /opt/wex`
- Execute `sudo bash /opt/wex/install`
- Check install with `wex hi`

# Install on mac

- Install XCode
- Install brew
- Update your bash and coreutils with `brew install bash coreutils`
- Then see Ubuntu installation process below

## Core extension

When a script is not found in the main script, it will ask for an action into the `project/extend` directory.

### project/extend/draft

It contains scripts used in production but waiting to e validated.

### project/extend/local

It contains scripts used locally. Theses script will never be versioned.

### project/extend/v2

It contains the previous version of the script for compatibility reason.

# MacOS compatibility

Tips to write compatible scripts.

- Do not use "readlink", prefer 
- For sed :
  > Use `wex file/regex` in place of `sed -i ... filename`
  > Use -E option instead of -r (BSD format)
