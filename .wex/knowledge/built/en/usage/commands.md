## Running a command

A command is one word made of three parts — the addon, the group and the name:

```bash
wex core::ping/hi        # hi!
wex core::version/get    # 6.0.134
```

The addon prefix is optional when the group and name are unambiguous, so `ping/hi`
resolves to the same command. Every part uses hyphens, never underscores:
`system::process/by-port`, not `by_port`. The kernel rejects the underscore form and
suggests the correct spelling.

Tab-completion is registered by the installer, so pressing `<Tab>` mid-command lists the
matching groups and names.

## Where commands come from

The prefix tells the kernel where to look. Four namespaces coexist:

| Form | Example | Lives in |
| --- | --- | --- |
| `addon::group/command` | `core::ping/hi` | the addon's `commands/` directory |
| `.group/command` | `.deploy/staging` | `.wex/commands/` of the current project |
| `~group/command` | `~test/hello` | `~/.wex/commands/` |
| `@service::group/command` | `@mysql::db/dump` | the matching service addon |

Addon commands are scanned once and cached. Project and user commands are re-read at
every run, so a file you just created is immediately callable.

## Options

Each command declares its own options, with a long and usually a short form. Ask any
command what it takes:

```bash
wex system::process/by-port --help
```

```
Usage: system::process/by-port [OPTIONS]
Return info about the process listening on a port
Options:
  --port, -p  <int>  [required]  Port number
  --help, -h  Show this message and exit.
```

```bash
wex system::process/by-port -p 6543
```

A handful of options are understood by every command, because they are handled by the
kernel rather than by the command:

| Option | Effect |
| --- | --- |
| `--quiet` | silence the interface — progress, prompts, logs |
| `-vv`, `-vvv` | raise verbosity; `-vvv` prints full tracebacks instead of a crash report path |
| `--output-format` | render the response as `str` (default) or `json` |
| `--output-target` | send the response to `stdout`, `file`, or `none` |
| `--output-file` | write the response to a given path, implies `--output-target file` |

`--quiet` silences the interface, not the result: `wex core::ping/hi --quiet` still prints
`hi!`. What a command returns is data, and data is never suppressed by a display flag.

## Writing your own

`core::command/create` scaffolds the file at the right place, in Python or as a YAML
workflow:

```bash
wex core::command/create --command "~notes/open" --extension py
```

The file path and the function name are both the command address, spelled differently:
`~notes/open` becomes `~/.wex/commands/notes/open.py` holding a `user__notes__open()`
function. There is no registration step — the resolver finds it by scanning.
