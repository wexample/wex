# Response System

## v5 reference

`wex-5/src/core/response/`

## Response types

- [ ] `AbstractResponse` — base with rendering logic
- [ ] `DefaultResponse` — plain text
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

## Rendering pipeline

- [ ] Render mode selection (terminal / json / none)
- [ ] Parent/child response chaining
- [ ] Output printing

## v6 target

- `wex-core`
