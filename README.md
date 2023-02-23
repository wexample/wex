# wex v4.0.8

A single command to execute your bash scripts, and a pattern to write it. See description for more info.

Join our community, support us, and find work at https://wexample.com 🤝❤️👨‍💻

## Install

### Ubuntu

- One line install : `sudo git clone --depth=1 https://github.com/wexample/wex.git /opt/wex && sudo bash /opt/wex/install`
- Check install : `wex hi`

Other platforms has not been tested yet for these version.

## Description

This is a mini-framework written in bash. This framework allows for the faster construction of bash scripts with a more organized structure. It provides useful tools for script management, such as reading command line arguments, generating automated documentation for scripts, and handling errors.

The usage is as follows:

    wex [?addon|default::][group]/[name] -a=firstArgWithShortName --second=secondArgWithLongName

### Cheat sheet

This is the most common commands used by core, but :
- For app management see [apps addon](https://github.com/wexample/wex-addon-app).
- For all other features, see `wex-service` addons in [repositories](https://github.com/orgs/wexample/repositories).

```bash
# Update core and addons.
wex core/update
# Display current version.
wex core/version
```

## Why using wex scripts

- You want to write some bash scripts on your local machine, and use it anywhere using a single command format
- You want to use some practical core builtin scripts. You can explore builtin scripts in the [/bash/](/bash/) directory.
- You want to use any `wex-service` addon available on our [repositories](https://github.com/orgs/wexample/repositories).

## Releasing a new version

Before pushing changes, you need to execute this command to update core feature and ensure stability :
  
  # Execute all tests : warning, this may download all docker images of services
  # you should probably run this command on a dedicated machine, virtual or not,
  # or a dedicated machine for scripts development.
  - wex test
  # Create internal registry and update version number
  - wex core/build

## Testing

### Creating test
    
    # Create a new unit test.
    wex test group/name create

### Running tests

    # Run all tests.
    wex test
    # Run only the test suite for the "wex file/linesCount" built-in script.
    wex test file/linesCount
