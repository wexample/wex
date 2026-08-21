# Roadmap : Réorganisation de la documentation

Opened: 2026-08-19
Updated: 2026-08-21

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

## The three axes

The work runs on three fronts at once, and none of them is out of scope — only the
order varies:

1. **Reading it** — every way the documentation is consulted: the generated README,
   `AGENTS.md`, agent tools, and the two surfaces still to build (CLI consultation and
   search, cases F and G below).
2. **Writing it** — every way it is produced: the template cascade, the composer,
   mandatory pages, contracts, and filestate delegating a file's content to an agent.
3. **Fixing it, one document at a time** — the individual passes over each project's
   knowledge, which is the only thing that turns a working mechanism into a
   documentation that is actually true.

Progress on one axis exposes the others: the composer (2) made the orphaned README
fragments visible (3), and rendering `wex`'s README (1) is what forced the mandatory
pages (2).

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
`contributing/{architecture,environment-variables,output,venv}.md.j2`,
`readme/_content.md.j2`, `specifications/vision.md.j2`,
`usage/{overview,addons,commands,installation,testing,uninstall,webhooks}.md.j2`.

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
(details above). Was **underfed**: only read `readme/`, never `usage/`,
`contributing/` or `specifications/`; no produced data entered it.
→ Addressed in phase 5: the `_content.md.j2` composer imports any knowledge page by
name, and `addons()` is the first produced data injected.

**B. `AGENTS.md` / `CLAUDE.md` — the agent that does not know wex.**
Hardcoded Python string (`with_ai_workdir_mixin.py:15`), written into each workdir,
now saying "browse `.wex/knowledge/`". This is what replaces the deleted
entrypoints/summaries, and it knows nothing of the actual folder contents.

**C. The human who opens the file.** Works, nothing to do.
Constraint to keep in mind: **a fragment converted to `.j2` is no longer readable in
place**. That is the price of templating; to be decided folder by folder, not
globally. Status quo for now, and case F removes the constraint outright.

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

**F. CLI consultation — to be built.** Reading a document from the terminal without
opening the file: `wex` serves the *built* version, not the source. Which settles the
constraint recorded in case C, since a `.j2` fragment unreadable in place becomes
readable through the command. And since the page passes through a render, that render
can do more than substitute variables — translating into the reader's language is the
first case to plan for, given that the knowledge is written in English while the author
works in French.

**G. Search — to be built.** Finding a feature across a suite of 89 packages, which no
current surface allows: `_knowledge_index()` lists identifiers, `knowledge/read`
resolves an exact path, and neither answers "which package handles X". This is where
the documentation stops being a set of files and becomes queryable.

The same commands serve both audiences: exposed as MCP tools, they close gap D — an
agent stops guessing a path and asks a question. Which makes F and G the natural
sequel to B rather than a side project.

**What the map shows**: one aggregator (A) and one complete agent circuit (E), with a
gap (D) in between, and two surfaces still missing (F, G). Properly addressing A forces
defining the reusable building block — multi-level resolution + j2 rendering + produced
data injection — that B, D, F and G all need.

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

## Phase 2 — Cleanup ✅

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

- [x] Migrations `6.0.130-1` (deletion of `documents/`) and `6.0.130-2` (deletion of
      `__entrypoint.md`) propagated
- [x] `PACKAGES/PYTHON/.wex/knowledge/todo/` → `.wex/journal/todo/` (7 tickets), and
      the empty `project-info/` left behind by phase 1 removed

Then swept across the Python packages — 21 out-of-convention files audited, 13 of which
already conformed. The inventory is now **empty**:

- [x] **Deleted**: `filestate/.wex/doc/{_entrypoint,_summary}.md` and
      `doc/project-info/_summary.md` (navigation files, phase 1 convention);
      `event/knowledge/dev/roadmap.md` (checked against the code — `Event`,
      `dispatcher`, `listener`, `priority`, `dispatch_event_async`, `EventPriority` all
      shipped); `prompt/knowledge/{changelog,migration}/0.0.22.md` (package is at
      14.1.0); `filestate/doc/project-info/project-conventions.md` (superseded by
      `option.md`)
- [x] **Moved to `journal/todo/`**: `api/knowledge/dev/rework.md` →
      `abstract-gateway-rework.md`, plus `helpers`' and `wex-addon-ai`'s stray
      `knowledge/todo/` tickets
- [x] **Moved into the convention**: `wex-core/knowledge/features/app-level-command.md`
      → `usage/`; filestate's 6 `.wex/doc/readme/` fragments →
      `usage/{concepts,configuration,features,options}.md` +
      `contributing/{operations,option-testing}.md`, which retires `.wex/doc/`
      entirely; `prompt/knowledge/package.md` split along the usage / contributing
      seam it straddled

Out of scope, deliberately: the README fragments orphaned by the composer (discovery is
bypassed when `_content.md.j2` exists), ~370 lines across `wex-addon-app`,
`packages/{app,event,orm,prompt}` and the suite. Resolved elsewhere.

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

Answered by the contracts system rather than by a single reference document: the
rules live next to the file they govern, and an agent receives only those that apply.

- [x] Per-file-type rules: `AbstractFormatter.get_writing_rules()`, keyed by
      `formatter:` in the contract. `AppDocFormatter` holds the knowledge-page rules
      (Jinja, `path()`, `##` headings, no own title)
- [x] Per-file rules: `.wex/ai/contracts/<mirrored path>.contract.yml`, with an
      `instructions` block per agent (`author`, `maintainer`) and `sources:` acting as
      change triggers. 13 contracts cover `wex`'s knowledge
- [x] Anti-rot: the `path()` Jinja global echoes a repository path and raises when it
      is gone, so a moved file becomes a build error instead of silent drift.
      `AppDocFormatter.extract_sources()` reads those calls back to propose contract
      sources
- [x] `contributing/architecture.md.j2` rewritten (kernel, addons, command resolution)
- [ ] Improve the `path()` failure message: currently surfaces as a generic
      `UNEXPECTED_ERROR`, the missing path only appears in the crash report

## Phase 5 — README + templating multi-app

First reading case addressed (case A), and the pretext for extracting the common
building block.

- [x] Restore `wex`'s README, and decide what feeds it beyond `readme/`: a
      `_content.md.j2` composer, which when present *is* the README (discovery is
      bypassed). It imports pages with `{{ knowledge('usage/commands') }}` — so
      `usage/` and `specifications/` feed the README by explicit import, not by rule
- [x] Composer inherited rather than duplicated: `{% extends "_layout.md.j2" %}` and
      `{% include %}` resolve across the whole 4-level cascade, so a single
      `_content.md.j2` in the suite's `package-readme/` governs all 89 packages with
      no file in any repository. Incidentally fixed a bug where every package README
      rendered its entire body twice (duplicate entry in `readme.sections`)
- [x] Two-pass table of contents: `toc()` emits a marker, `_build_toc()` then parses
      the level-2 headings of the *rendered* output, so anchors cannot lie
- [x] Inject produced data — first case: `addons()`, the addon table read from the
      installed distributions' metadata
- [x] Mandatory knowledge pages declared by the workdir hierarchy:
      `get_required_knowledge_pages()` on `ManagedWorkdir` (`usage/overview`,
      `contributing/architecture`), extended by `PythonPackageWorkdir`
      (`usage/quickstart`). A required set, not an allowlist — a floor, not a ceiling.
      Seeded through `default_content`, so a written page is never overwritten, and
      the stub is a Jinja comment so an unwritten page renders to nothing rather than
      leaking a `TODO` into a README published to PyPI
- [ ] Generalise multi-level aggregation to any target, not just README
- [ ] Have `AGENTS.md` / `CLAUDE.md` produced by this system (case B)
- [ ] Open a reading path on the app's `.wex/knowledge/` (case D)
- [ ] Switch remaining `.md` fragments to `.j2` — weigh against case C
- [ ] Decide whether exported `.md` files are versioned generated artefacts or not
- [ ] `readme.sections` in `PACKAGES/.wex/config.yml` is now dead for composer-based
      packages: remove it, or keep it for the legacy discovery path?

## Phase 6 — Consultation and search commands

Two new command families, which are the concrete form of "how the documentation is
searched". Written once, they serve the human at the terminal and the agent through
MCP — the surface distinction of case E applies, not a second implementation.

**Consultation (case F)**

- [ ] `wex` reads a document by identifier and serves the **built** version: the
      cascade resolved, the Jinja rendered, the produced data injected. Never the raw
      source, which is what makes the `.j2` question of case C moot
- [ ] Rendering is a transformation stage, not just variable substitution: translating
      into the reader's language is the first case to plan for, the knowledge being
      written in English while the author works in French
- [ ] Decide where a built version is cached, and what invalidates it

**Search (case G)**

- [ ] Find a feature across a suite of 89 packages — "which package handles X" — which
      no current surface answers
- [ ] Decide the mechanism: index built at rectify, full-text over the built versions,
      or an agent reading the index. Weigh against the fact that the corpus is
      generated, so the index can be a build product rather than a service
- [ ] Expose both families as agent tools, which closes gap D: an agent stops guessing
      a path and asks a question

**Prompts**

- [ ] Define the composition of an agent prompt: fragments + context compiled on the
      fly (project structure, dependencies, available commands…)
- [ ] Reuse the same aggregation building block as the documentation
- [ ] Pick up the tag taxonomy (`suite@99e98dd`) for MCP filtering

## Phase 7 — Enrich the documentation

- [x] `wex`: `usage/{overview,addons,commands}` written, `usage/testing` corrected
      (documented a `test::run/all` that does not exist, and a fictional test tree),
      `usage/environment-variables` moved to `contributing/`, heading levels demoted
      in 5 files so they reach the composer's table of contents
- [x] The 37 Python packages rectified: README rebuilt and the three mandatory pages
      present everywhere, none left as a stub. The remaining repositories are the
      non-Python ones, whose language addons ship no `install` template yet
- [x] Stubs filled by the `author` agent, contract in hand. Wiring it to filestate, so
      a declared file has its content written by an agent, is tracked outside this
      roadmap

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

Phases 1, 2 and 4 complete, phase 5 case A complete, phase 7 complete for Python.
The whole chain has now run at scale: the 37 Python packages each have a rebuilt
README and the three mandatory pages written — not one left as a stub. Which is the
proof the mechanism was built for, the composer having to hold across 37 repositories
without a file in any of them.

Read against the three axes: **writing it** and **fixing it** are both done for the
Python suite. **Reading it** has one working surface out of the five mapped, and is
now the bottleneck.

Next step: phase 6, whose two command families (consultation and search, cases F and
G) are what make a corpus of this size usable at all. They share the aggregation
building block that case A just proved, as do case B (`AGENTS.md`) and case D (agents
reading the app's own knowledge). The non-Python repositories follow, once their
language addons ship the templates the Python one has.

Still open, unrelated to the phases:
- `dev-css` ships an empty `description`; `dev-javascript` and `dev-php` both claim
  "Python dev addon for wex"
- `_get_project_license()` reads `license` at the top level of `pyproject.toml`,
  where the field is `project.license`
