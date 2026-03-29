# Response System

## Architecture decisions (v6)

### Three distinct output concerns

| Concern | What it is | v6 mechanism |
|---|---|---|
| **Response** | The data produced by a command | Response types (`DictResponse`, `ListResponse`, …) |
| **Prompt** | Interactive UI — progress bars, confirmations, questions | `wexample-prompt` package, `context.io.*` |
| **Log** | Operational/diagnostic messages (debug, info, warning, error) | `context.io.log()` → stderr / log file (to clarify) |

These three must stay separate. A command that returns a `DictResponse` is producing **data**. A command that calls `io.log("starting…")` is emitting a **log**. A command that calls `io.confirm("sure?")` is doing a **prompt**. They may all happen in the same command, but they go to different destinations and have different consumers.

### "Render mode" is dead — replaced by two orthogonal axes

v5 conflated format + destination into one `render_mode`. v6 separates them cleanly:

- **`output_format`** (`str` | `json`) — *how* the response is serialised
  - `str` → human-readable, for the terminal
  - `json` → machine-readable, for piping to other scripts or tools
- **`output_target`** (`stdout` | `file` | `none`) — *where* it goes
  - `none` → evaluate the command but suppress all output (used for internal calls and tests)

v5 mapping:
- `KERNEL_RENDER_MODE_TERMINAL` → `output_format=str` + `output_target=stdout`
- `KERNEL_RENDER_MODE_JSON` → `output_format=json` + `output_target=stdout`
- `KERNEL_RENDER_MODE_NONE` → `output_target=none` (format irrelevant)

### Consequence for response types

Each response type must implement format-aware rendering:
```python
def render(self, output_format: str) -> str:
    if output_format == "json":
        return json.dumps(self.content)
    return self._render_str()   # human-readable default
```
`output_target=none` is handled upstream — the response is never asked to render.

### On logs

`context.io.log()` currently mixes logs and prompt feedback. To clarify later:
- Logs (diagnostic) → should go to stderr or a log file, not stdout
- The response pipeline should never write to stdout directly — that is the output handler's job

---

## v5 reference

`wex-5/src/core/response/`

## Already in v6 (wexample-app)

- [x] `NullResponse` — `response_normalize(None)` → already used by ping/pong test
- [x] `BooleanResponse` — `response_normalize(bool)` + `__attrs_post_init__` type check
- [x] `DefaultResponse` — `response_normalize(Any)`
- [x] `MultipleResponse` — container used by middleware execution
- [x] `FailureResponse` — used in middleware stop-on-failure
- [x] `response_normalize()` — central dispatcher (wexample-app/helpers/response.py)
- [x] `StrResponse` — `wexample_app/response/str_response.py`, enforce `isinstance(str)`
- [x] `IntResponse` — `wexample_app/response/int_response.py`, enforce `isinstance(int)`

## Render modes

v5 had 3 render modes passed as argument to every `response.print()`:
- `KERNEL_RENDER_MODE_TERMINAL` — human-readable text
- `KERNEL_RENDER_MODE_JSON` — machine-readable JSON
- `KERNEL_RENDER_MODE_NONE` — no output (lazy evaluation, used in tests and piped calls)

Each response type implements its own rendering per mode.
**v6 — déjà en place** : `output_format` (str/json/yaml) sur `CommandRequest`, défaut `str` sur le kernel, dispatché dans `AbstractResponse.get_formatted()` → `_get_formatted_json_content()` / `_get_formatted_yaml_content()` / `_get_formatted_prompt_response()`.

## Response type hierarchy

```
AbstractResponse (base)
├── AbstractEmptyResponse
│   └── AbortResponse                    — stops execution with reason [SKIP]
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
- [x] `DictResponse` — `wexample_app/response/dict_response.py`, title optionnel, PropertiesPromptResponse
- [x] `ListResponse` — `wexample_app/response/list_response.py`, title optionnel, ListPromptResponse
- [x] `TableResponse` — `wexample_app/response/table_response.py`, headers + rows
- [x] `KeyValueResponse` — **SKIP** : fusionné dans `DictResponse` (même rendu via PropertiesPromptResponse)
- [~] `AbortResponse` — **SKIP** : redondant avec `QueuedCollectionStopResponse` + exceptions Python

### Phase 2 — special behaviours
- [x] `HiddenResponse` — **SKIP** : remplacé par `output_target=none`
- [x] `FunctionResponse` — `wexample_app/response/function_response.py` — `content: Callable[[], AbstractResponse]`, lazy + cached, le contenu est n'importe quel callable (pas lié à `run_function`)
- [x] `ShellCommandResponse` (ex-NonInteractive) — `wexample_app/response/shell_command_response.py`
- [x] `InteractiveShellCommandResponse` — `wexample_app/response/interactive_shell_command_response.py`

### Phase 3 — collections
- [x] `ResponseCollectionResponse` — `wexample_app/response/response_collection_response.py`
- [x] `QueuedCollectionResponse` — `wexample_app/response/queued_collection_response.py`, pipeline `previous_value`, `QueuedCollectionStopResponse`, `QueuedCollectionStopCurrentStepResponse`. Fast mode supprimé.

> **Future idea — parallel execution** : `ParallelCollectionResponse` as a separate response type for concurrent steps. Out of scope for now, to be designed independently.

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
