This project is managed by **wex**, which keeps its documentation, its journal and its
agent configuration under `.wex/`.

## Documentation

Read `.wex/knowledge/built/en/`, which is the rendered prose. The `.md.j2` files above it
are the templates it is built from, and are not meant to be read directly.

## If `wex` is installed

`wex hi` prints `hi!` when it is. Four commands then reach past this repository, into the
packages around it that are not visible from here. Each takes `--query <text>` and
`--scope self|suite|stack`, and answers with where to look rather than with the answer:

```bash
wex app::knowledge/search --query <text>   # the documentation of every package
wex app::journal/search   --query <text>   # the notes, tasks and subjects recorded in them
wex app::source/search    --query <text>   # the code they ship
wex ai::session/search    --query <text>   # the conversations already held there
```

Every answer ends on what was actually reached, so a scope covering one app is never read
as covering the stack. Run the first before concluding a subject is undocumented, the
second before opening a task that may already exist, the third before writing a class a
sibling package already has.

`wex ai::agent/talk` opens a session with those commands wired in as tools.

## If it is not

Nothing above is required to work here: `.wex/knowledge/built/en/` is plain markdown, and
the repository reads like any other. Installing wex is documented at
https://github.com/wexample/wex.
