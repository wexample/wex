# wex v4.0.0

A single command to execute your bash scripts, and a pattern to write it.

Join our community, support us, and find a job at https://wexample.com 🤝❤️👨‍💻

## Install

### Ubuntu

- One line install : `sudo git clone --depth=1 https://github.com/wexample/wex.git /opt/wex && sudo bash /opt/wex/install`
- Check install : `wex hi`

## Why using wex scripts

- You want to user some practical core builtin scripts (i.e. `wex system/os` return "**linux**"). You can explore builtin scripts in the [/project/bash/default/](/project/bash/default/) directory.

## Why using wex scripts

- You want to user some practical core builtin scripts (i.e. `wex system/os` return "**linux**"). You can explore builtin scripts in the [/project/bash/default/](/project/bash/default/) directory.

## Running tests

    # Run all tests.
    wex test
    # Run only the test suite for the "wex file/linesCount" built-in script.
    wex test file/linesCount