from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any, Iterable, List, Optional

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
            kernel.io.log(f"{title} : {step.__name__}")

            response = step()

            click.echo(os.linesep)

            # Step failed somewhere
            if response is False:
                return


def prompt_choice(
    question: str,
    choices: List[str | Choice],
    default: Optional[InquirerPyDefault] = None,
    **kwargs: Any,
) -> Any:
    choices_all = choices.copy()
    choices_all.append(Choice(value=None, name="> Abort"))

    return inquirer.select(  # type: ignore
        message=question, choices=choices_all, default=default, **kwargs
    ).execute()
