# Response System

> ⚠️ Paradigm change: v5 response objects are replaced in v6 by `ExecutionContext` + output handlers.
> Before migrating individual types, decide which v5 responses map to v6 output patterns vs which need new equivalents.

## v5 reference

`wex-5/src/core/response/`

## v6 equivalent (already in place)

- [x] Output handlers: `stdout` / `file` / `none` — pluggable, set via `--output_format` / `--output_target`
- [x] `ExecutionContext` — provides `io.log()`, `io.progress()`, access to kernel and request

## Response types to migrate or replace

- [ ] `DefaultResponse` — plain text → `io.log()`?
- [ ] `DictResponse` — dictionary output
- [ ] `ListResponse` — list output
- [ ] `TableResponse` — table formatting
- [ ] `KeyValueResponse` — key-value pairs
- [ ] `FunctionResponse` — wraps function return value
- [ ] `InteractiveShellCommandResponse` — interactive shell execution
- [ ] `NonInteractiveShellCommandResponse` — non-interactive shell
- [ ] `HiddenResponse` — suppressed output
- [ ] `NullResponse` — no output
- [ ] `AbortResponse` — signals command abort
- [ ] `ResponseCollectionResponse` — multiple responses
- [ ] `QueuedCollectionResponse` — queued response execution

## v6 target

- Simple output → `ExecutionContext.io`
- Structured output → to define (new response classes in wex-core, or a dedicated pattern)
