# wex v4.0.20

A single command to execute your bash scripts, and a pattern to write it. See description for more info.

Join our community, support us, and find work at https://wexample.com 🤝❤️👨‍💻

## Install

### Ubuntu

One line install : 

    sudo git clone --depth=1 https://github.com/wexample/wex.git /opt/wex && sudo bash /opt/wex/install

Check install : 

    # Returns : hi!
    wex hi

Other platforms has not been tested yet for these version.

## Description

This is a mini-framework written in bash. This framework allows for the faster construction of bash scripts with a more
organized structure. It provides useful tools for script management, such as reading command line arguments, generating
automated documentation for scripts, and handling errors.

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
- You want to use some practical core builtin scripts. You can explore builtin scripts in the [/bash/](/bash/)
  directory.
- You want to use any `wex-service` addon available on our [repositories](https://github.com/orgs/wexample/repositories)
  .

## Core organization

### Main folder structure

The wex scripts folder is organized as follows:

- The bash folder contains the core scripts, essential for basic operation (calling commands, addons, updates, etc.).
- The "addons" folder contains the addons, each of which has an associated folder and Git repository. Each addon folder
  has the same structure as the root wex scripts folder (except for the addons folder, there are no addons within an
  addon).
- The includes folder contains the functions necessary for the proper functioning of the scripts.
- The tests folder contains the functional and unit tests executed using `wex test`.

### Structure of the bash folder

The scripts themselves are organized as follows:

- Each folder corresponds to a group.
- Each file name corresponds to the script name (excluding the .sh extension).

### Structure of .sh files

- Each .sh script contains at least one function, with the following schema: groupNameScriptName() { ... }
- There may be a function defining the arguments, with the following schema: groupNameScriptNameArgs() { ... }

#### Structure of configuration functions

    groupNameScriptNameArgs() {
      _ARGUMENTS=(
        # [Long name] [Short name] [Argument description] [Required] [Default value]
        'long_name ln "Argument description" false "abc"'
      )
      _AS_NON_SUDO=false
      _DESCRIPTION="Description of the script"
    }

- The configuration function will transform each argument into a Bash variable in screaming snake case, for example:
  ${LONG_NAME}.
- If an argument is missing, it will be interactively prompted to the user.
- Other arguments are always added to the customized list, use the `--help` argument to see them.

## Releasing a new version

Before pushing changes, you need to execute this command to update core feature and ensure stability :

Execute all tests : warning, this may download all docker images of services you should probably run this command on a
dedicated machine, virtual or not, or a dedicated machine for scripts development.

    wex test

Create internal registry and update version number

    wex core/build

## Testing

### Creating test

    # Create a new unit test.
    wex test group/name create

### Running tests

    # Run all tests.
    wex test
    # Run only the test suite for the "wex file/linesCount" built-in script.
    wex test file/linesCount
