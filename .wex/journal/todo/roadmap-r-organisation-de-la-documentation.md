# Roadmap : Réorganisation de la documentation

Opened: 2026-08-19
Updated: 2026-08-19

**Single place for this work.** Everything related to the documentation system is
managed here. Consolidates `.wex/knowledge/state-of-the-art.md` and
`.wex/knowledge/knowledge-system-proposal.md` (deleted).

Starting problem: very little documentation has been written and the author is lost
in it. The goal is a single convention applied everywhere, and documentation maintained
as automatically as possible from the code.

---

## Retained principles

1. **Single source of truth** — a piece of information exists in one place only. The
   rest is generated, imported or referenced.
2. **Generation > manual writing** — what can be produced by template must be.
   Applied corollary: every hand-written navigation file (`__entrypoint.md`,
   `__summary.md`) is deleted; they will be regenerated if the need is confirmed.
3. **wex as the primary interface** — agents explore through wex commands; the
   knowledge is the human-readable cache for those without access.
4. **Convention over configuration** — same structure everywhere; variants are
   additions, not exceptions.
5. **`knowledge/` = timeless, `journal/` = dated.**

---

## Target structure of `.wex/knowledge/`

```
knowledge/
├── readme/          # .md.j2 fragments → generated README
├── usage/           # using the project without modifying it
├── contributing/    # modifying / extending it (humans + agents)
└── specifications/  # lasting reference (vision, constraints, contracts)
```

At suite level, `package-readme/` is added (fragments inherited by child packages).
A compromise name, to be renamed eventually.

State reached in `wex` — compliant:
`contributing/{architecture,output,venv}.md`, `readme/introduction.md`,
`specifications/vision.md`, `usage/{introduction,testing,webhooks,environment-variables}.md`.

---

## State of the art (verified in the code)

**1. README templating is already good, just underused.**
Chain: `AggregatedTemplatesConfigValue` → `ReadmeContentConfigValue` →
`AppReadmeConfigValue` → `PythonPackageReadmeContentConfigValue`.
4-level lookup (workdir → language addon → app addon → ancestor suites),
sections discovered by `.md.j2`/`.md` file, order driven by `readme.sections`
in the suite's `config.yml`, rendered by Jinja2 with custom filters
(`helpers/jinja.py:9`, multi-path `ChoiceLoader`).
This is the building block to generalise, not to rewrite.

**2. `AGENTS.md` / `CLAUDE.md` are not composed.**
`with_ai_workdir_mixin.py:15` — `build_agents_content()` returns a hardcoded Python
string; `CLAUDE.md` is a one-line pointer (`CLAUDE_POINTER_CONTENT`).
The intention behind the now-deleted `knowledge/documents/{readme,agents}` was
probably to produce them from `.j2` files: picked up again in phase 5.

**3. Migrations exist but have not been propagated.** A recurring observation:
`6.0.112-2` (roadmap → journal) never ran on several packages, and the two new ones
only ran on `wex`.

---

## Reading paths (verified inventory)

Who reads the knowledge, by what mechanism, and in what state. This is the map that
drives phases 5 and 6.

**A. Generated `README.md` — the only aggregator in working order.**
`AppReadmeConfigValue`, triggered at `state/rectify`. 4-level lookup, Jinja2 rendering
(details above). **Underfed**: only reads `readme/`, never `usage/`, `contributing/`
or `specifications/`; no produced data (commands, services, child packages) enters it;
`wex` has only one fragment left.
→ First case to address.

**B. `AGENTS.md` / `CLAUDE.md` — the agent that does not know wex.**
Hardcoded Python string (`with_ai_workdir_mixin.py:15`), written into each workdir,
now saying "browse `.wex/knowledge/`". This is what replaces the deleted
entrypoints/summaries, and it knows nothing of the actual folder contents.

**C. The human who opens the file.** Works, nothing to do.
Constraint to keep in mind: **a fragment converted to `.j2` is no longer readable in
place**. That is the price of templating; to be decided folder by folder, not
globally. Status quo decided for now.

**D. wex agents — the gap.** Two surfaces:
`_knowledge_index()` (`abstract_agent.py:677`) lists `<service>:<section>` identifiers
in the system prompt without reading the content; `app::knowledge/read`
(`AGENT_SAFE`) resolves `find_service_dir()` then reads `<service_dir>/knowledge/<section>.md`
as plain text, without template rendering.
**Both only target the knowledge of *services*. The app's own `.wex/knowledge/` has
no programmatic reading path** — an agent cannot reach `contributing/architecture.md`.
Alongside this, the `context.j2` cascade (5 levels, `abstract_agent.py:444-558`) is
the only precedent for context compiled at read time, but it only renders files
literally named `context.j2` (`_render_context_template():1335`) and never injects
any knowledge.

**E. `journal/todo|done` — the only complete circuit.**
`todo/write|done|list` are `HUMAN_ONLY` **deliberately** (`todo/write.py:45`): agents
access them through the `todo_write`/`todo_list` tools, which also manage the topic
stack. `analysis/report` is the `AGENT_SAFE` counterpart, writing to `journal/analysis/`.
**There are therefore two distinct exposure surfaces** — MCP commands filtered by
tags, and dedicated agent tools — not to be confused in phase 6.

**What the map shows**: one aggregator (A) and one complete agent circuit (E), with a
gap (D) in between. Properly addressing A forces defining the reusable building block
— multi-level resolution + j2 rendering + produced data injection — that B and D need.

---

## Phase 1 — Folder structure ✅

- [x] `knowledge/documents/{readme,agents}` deleted: created everywhere, read by
      nothing. The surviving convention is `knowledge/readme` +
      `knowledge/package-readme`, now declared in `managed_workdir.py`
- [x] `coding/` + `code-style/`, `project/` + `project-info/`, `tools/` dissolved
- [x] `__entrypoint.md` removed from the filestate declaration (created empty in 82
      workdirs) and deleted
- [x] `__summary.md` / `_summary.md` deleted — the reference in `AGENTS.md`
      (`with_ai_workdir_mixin.py:32`) pointed to a file that barely existed anywhere,
      replaced by "browse `.wex/knowledge/`"
- [ ] Rename `package-readme/` ?

## Phase 2 — Cleanup

Done in `wex` and the `PACKAGES/PYTHON` suite:

- [x] `knowledge/migration/` deleted (v5→v6 complete, 27 files)
- [x] **Obsolete files deleted**: `dot-wex-directory.md` (described `.wex/bash/` and
      `.wex/doc/`, gone), `tools/wex.md` ("Current version: 5.x"),
      `tools/{maintenance-scripts,package-management}.md` (documented
      `for_all_package.sh` / `for_all_venv.sh`, non-existent scripts),
      `project-info/{project-conventions,project-structure}.md` (no content),
      `contributing/exporting-skeleton.md` (duplication procedure using `_copy`,
      old convention)
- [x] `wex_command_tags.md` deleted — 385-line agent output of which 233 were a
      command inventory, stale at the first addition. **Section 3 is a proposed but
      unapplied tag taxonomy**; tags already serve MCP filtering
      (`DEFAULT_EXCLUDED_TAGS = {"human-only"}`, `wex-addon-ai/helpers/mcp.py`).
      To be recovered for phase 6: `suite@99e98dd`
- [x] **Moved**: `coding/output.md` → `contributing/`, `coding/python/venv.md`
      → `contributing/`, `project/vision.md` → `specifications/`,
      `project/architecture.md` → `contributing/` (wex);
      `project-info/{typed-config-files,app-manager-folder,pip-packages-structure}.md`
      → `contributing/` (suite)

Remaining:

- [ ] Migration: `PACKAGES/PYTHON/.wex/knowledge/todo/` → `.wex/journal/todo/` (7 tickets)
- [ ] Propagate migrations `6.0.130-1` (deletion of `documents/`) and `6.0.130-2`
      (deletion of `__entrypoint.md`): ~84 workdirs, all empty. Decide on the vector —
      suite-wide command or incrementally via `rectify`
- [ ] Polluted knowledge in other packages: case by case, outside this work.
      Heaviest case identified: `packages/filestate/.wex/doc/` (v5 remnant) holds
      498 lines of orphaned README fragments, while its `README.md` (477 lines) is
      frozen and cannot be regenerated

## Phase 3 — Move code rules into the language package

Deleted from `wex` and the suite, **to be redone** in `wex-addon-dev-python` as
documentation for the rectify options that already enforce them (`FormatOption`,
`ModernizeTypingOption`, marker `# filestate: python-iterable-sort`).
Original content recoverable from: `wex@7cffc16c4`, suite `@74beedd`.

- [ ] `coding/general.md`, `coding/python/{sorting,spacing,typing,syntax}.md` (wex)
- [ ] `code-style/{general,python,maintenance-script}-code-style.md` (suite)

To be rewritten from the code, not copied: `python-code-style.md` still mentioned
Pydantic while the code has moved to attrs / `base_class` / `public_field`.

## Phase 4 — Define how each file is written

- [ ] For each file type: audience, expected length, tone, what belongs / what does
      not, when it is updated
- [ ] Make it a single, authoritative reference — the document that writing agents
      will read
- [ ] Rewrite `contributing/architecture.md` (30 lines that still describe wex as an
      "Installation Manager", with no mention of the kernel, addons, or command
      resolution)

## Phase 5 — README + templating multi-app

First reading case addressed (case A), and the pretext for extracting the common
building block.

- [ ] Restore `wex`'s README: currently a single fragment
- [ ] Decide what feeds the README beyond `readme/` — sections drawn from `usage/` /
      `specifications/`? references only?
- [ ] Inject produced data: commands, services, child packages
- [ ] Generalise multi-level aggregation to any target, not just README
- [ ] Have `AGENTS.md` / `CLAUDE.md` produced by this system (case B)
- [ ] Open a reading path on the app's `.wex/knowledge/` (case D)
- [ ] Switch remaining `.md` fragments to `.j2` — weigh against case C
- [ ] Decide whether exported `.md` files are versioned generated artefacts or not

## Phase 6 — Agent prompts with dynamic context

- [ ] Define the composition of an agent prompt: fragments + context compiled on the
      fly (project structure, dependencies, available commands…)
- [ ] Reuse the same aggregation building block as the documentation
- [ ] Pick up the tag taxonomy (`suite@99e98dd`) for MCP filtering
- [ ] Define how agents search the documentation, for themselves or for the USER

## Phase 7 — Enrich the documentation

- [ ] `wex` first, then module by module, package by package

---

## Leads to investigate (not decided)

- **Generate documentation from the code.** First concrete candidate: a document
  describing the `.wex/` tree, since `managed_workdir.prepare_value()` is the source
  of truth. The two hand-written `dot-wex-directory.md` files had drifted. Second
  candidate: the command inventory, see `wex_command_tags.md`.
- **One agent per documentation file**, responsible for keeping it current.
- **Propagation / export commands**: smart compilations, targeted display.
- **Link code and documentation**: watch diffs, or tag comments. Implies update
  lifecycles.
- **Reproducible standard**: check applicability outside the Python ecosystem
  (syrtis, PHP/JS packages).

---

## Status

Phase 1 complete, phase 2 complete for `wex` and the Python suite. `wex`'s
`knowledge/` conforms to the target structure (13 files, 4 folders).
Reading paths are inventoried and verified in the code.
Nothing is committed.
Next step: phase 5, case A (the `wex` README), which serves as the test bench for
the reusable aggregation building block.
