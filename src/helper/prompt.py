from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any, Callable, Iterable, List, Optional, cast

import click
from click._termui_impl import ProgressBar, V
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.utils import InquirerPyDefault

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


def prompt_build_progress_bar(steps: Iterable[V], **kwargs: Any) -> ProgressBar[V]:
    return click.progressbar(steps, fill_char="▪", empty_char="⬝", **kwargs)


def prompt_progress_steps(
    kernel: "Kernel", steps: Iterable[V], title: str = "Processing"
) -> None:
    with prompt_build_progress_bar(steps, label=title) as progress_bar:
        for step in progress_bar:
            step_callable = cast(Callable[..., Any], step)
            kernel.io.log(f"{title} : {step_callable.__name__}")

            response = step_callable()

            click.echo(os.linesep)

            # Step failed somewhere
            if response is False:
                return


def prompt_choice_dict(
    question: str,
    choices: dict,
    default: Optional[InquirerPyDefault] = None,
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
    abort: Optional = "> Abort",
    **kwargs: Any,
) -> Any:
    choices_all = choices.copy()

    if abort:
        choices_all.append(Choice(value=None, name=abort))

    return inquirer.select(  # type: ignore
        message=question, choices=choices_all, default=default, **kwargs
    ).execute()
