from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Iterable, List, Optional, cast

import click
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.utils import InquirerPyDefault
from click._termui_impl import ProgressBar, V

from src.const.types import StringsDict

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


def prompt_build_progress_bar(steps: Iterable[V], **kwargs: Any) -> ProgressBar[V]:
    return click.progressbar(steps, fill_char="▪", empty_char="⬝", **kwargs)


def prompt_progress_steps(
    kernel: "Kernel", steps: Iterable[V], title: Optional[str] = None
) -> None:
    previous_length = kernel.io.log_length

    with prompt_build_progress_bar(steps, label=title) as progress_bar:
        for step in progress_bar:
            step_callable = cast(Callable[..., Any], step)

            # Play with length to keep status after bar.
            kernel.io.log_length = 0
            kernel.io.log(f" {step_callable.__name__}")
            kernel.io.log_length = 10

            response = step_callable()

            # Step failed somewhere
            if response is False:
                return

            kernel.io.log_clear()

    kernel.io.log_length = previous_length


def prompt_choice_dict(
    question: str,
    choices: StringsDict,
    default: Optional[str] = None,
    **kwargs: Any,
) -> Any:
    items = choices.items()

    choice = prompt_choice(
        question,
        list(choices.values()),
        choices[default] if default else None,
        **kwargs,
    )

    return next((key for key, value in items if value == choice), default)


def prompt_choice(
    question: str,
    choices: List[Any | Any],
    default: Optional[InquirerPyDefault] = None,
    abort: Optional[str] = "> Abort",
    **kwargs: Any,
) -> Any:
    choices_all = choices.copy()

    if abort:
        choices_all.append(Choice(value=None, name=abort))

    return inquirer.select(  # type: ignore
        message=question, choices=choices_all, default=default, **kwargs
    ).execute()
