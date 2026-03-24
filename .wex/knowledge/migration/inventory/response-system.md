# Response System

## v5 reference

`wex-5/src/core/response/`

## Already in v6 (wexample-app)

- [x] `NullResponse` — `response_normalize(None)` → already used by ping/pong test
- [x] `BooleanResponse` — `response_normalize(bool)`
- [x] `DefaultResponse` — `response_normalize(Any)`
- [x] `MultipleResponse` — container used by middleware execution
- [x] `FailureResponse` — used in middleware stop-on-failure
- [x] `response_normalize()` — central dispatcher (wexample-app/helpers/response.py)

## Render modes

v5 had 3 render modes passed as argument to every `response.print()`:
- `KERNEL_RENDER_MODE_TERMINAL` — human-readable text
- `KERNEL_RENDER_MODE_JSON` — machine-readable JSON
- `KERNEL_RENDER_MODE_NONE` — no output (lazy evaluation, used in tests and piped calls)

Each response type implements its own rendering per mode.
**v6 decision needed**: map render modes to `output_format` (`--output_format str|json`) already on kernel.

## Response type hierarchy

```
AbstractResponse (base)
├── AbstractEmptyResponse
│   └── AbortResponse                    — stops execution with reason
├── AbstractTerminalSectionResponse
│   ├── DictResponse                     — dict as key: value lines
│   ├── KeyValueResponse                 — key-value with optional title
│   ├── ListResponse                     — list as line-separated output
│   └── TableResponse                    — table with headers + title
├── DefaultResponse (in wexample-app)
│   └── HiddenResponse                   — stored but not displayed interactively
├── FunctionResponse                     — wraps callable for lazy execution
├── InteractiveShellCommandResponse      — shell cmd with live stdout
├── NonInteractiveShellCommandResponse   — shell cmd, output captured
├── NullResponse (in wexample-app)
├── ResponseCollectionResponse           — ordered list of responses
└── QueuedCollectionResponse             — sequential steps with queue manager
    └── queue_collection/
        ├── AbstractQueuedCollectionResponseQueueManager
        ├── DefaultQueuedCollectionResponseQueueManager
        ├── FastModeQueuedCollectionResponseQueueManager
        ├── QueuedCollectionPathManager
        ├── QueuedCollectionStopResponse  — stops entire queue
        └── QueuedCollectionStopCurrentStepResponse
```

## Response types to migrate

### Phase 1 — simple structured output
- [ ] `DictResponse` — dict → formatted lines or JSON
- [ ] `ListResponse` — list → newline-separated or JSON array
- [ ] `TableResponse` — rows + headers + title
- [ ] `KeyValueResponse` — labelled key-value pairs with optional title
- [ ] `AbortResponse` — abort signal with reason (partially covered by FailureResponse?)

### Phase 2 — special behaviours
- [ ] `HiddenResponse` — content stored, not printed in terminal mode
- [ ] `FunctionResponse` — lazy callable wrapping
- [ ] `NonInteractiveShellCommandResponse` — capture shell output as response
- [ ] `InteractiveShellCommandResponse` — live shell output (tty passthrough)

### Phase 3 — collections (most complex)
- [ ] `ResponseCollectionResponse` — flat ordered list of responses
- [ ] `QueuedCollectionResponse` — sequential execution with:
  - `queue.get_previous_value()` — access previous step result
  - nested `QueuedCollectionResponse`
  - fast mode vs standard mode (subprocess comparison in tests)
  - `QueuedCollectionStopResponse` / `QueuedCollectionStopCurrentStepResponse`

## v5 test infrastructure (AbstractTestCase)

**Base class:** `wex-5/tests/AbstractTestCase.py`

Assertion helpers:
- `assertResponseFirstEqual(response, expected)`
- `assertResponseFirstContains(response, expected)`
- `assertResponseOutputBagItemEqual(response, index, expected)` — nth item
- `assertResponseOutputBagItemContains(response, index, expected)`
- `for_each_render_mode(callback, expected_per_mode)` — runs test across all 3 render modes
- `run_function(function, args, render_mode)` — executes a test command function

Response navigation (v5):
- `response.first()` / `response.last()` / `response.get(*indices)`
- `response.print_wrapped(render_mode)` / `response.print_wrapped_str()`

## v5 test files inventory

**Return type tests** (`wex-5/addons/test/tests/command/return_type/`):
- `dict.py`, `list.py`, `table.py`, `key_value.py`
- `function.py`, `hidden.py`
- `null.py`, `str.py`, `int.py`
- `queued_collection.py`, `response_collection.py`
- `interactive_shell_command.py`, `non_interactive_shell_command.py`

**Demo command tests** (`wex-5/addons/test/tests/command/demo_command/`):
- `responses.py` — basic response types
- `response_collection.py` — complex multi-step queued collection
- `response_collection_two.py` — nested collection
- `response_collection_three.py` — abort/stop responses
- `counting_collection.py` — iteration test

## Migration order (recommended)

1. Render modes → map to `output_format` on kernel
2. Phase 1: `DictResponse`, `ListResponse`, `TableResponse`, `KeyValueResponse`, `AbortResponse`
3. Phase 2: `HiddenResponse`, `FunctionResponse`, shell commands
4. Phase 3: `ResponseCollectionResponse`, then `QueuedCollectionResponse` (biggest)
5. Test base class equivalent (`AbstractTestCase` → pytest fixtures + helpers)
