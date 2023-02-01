# wex v4.0.0

A single command to execute your bash scripts, and a pattern to write it.

Join our community, support us, and find a job at https://wexample.com 🤝❤️👨‍💻

## Install

### Ubuntu

- One line install : `sudo git clone --depth=1 https://github.com/wexample/wex.git /opt/wex && sudo bash /opt/wex/install`
- Check install : `wex hi`

## Why using wex scripts

- You want to write some bash scripts on your local machine, and use it anywhere using a single command format : `wex my/script -a=arg --arg2=arg2`
- You want to use some practical core builtin scripts. You can explore builtin scripts in the [/bash/](/bash/) directory.
- You want to use any `wex-service` extension available on our [repository](https://github.com/orgs/wexample/repositories).

## Running tests

    # Run all tests.
    wex test
    # Run only the test suite for the "wex file/linesCount" built-in script.
    wex test file/linesCount
