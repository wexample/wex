from __future__ import annotations

from typing import TYPE_CHECKING, Optional, cast

from src.const.globals import VERBOSITY_LEVEL_MAXIMUM
from src.core.CommandRequest import CommandRequest, HasRequest
from src.core.response.AbstractResponse import AbstractResponse, HasResponse
from src.helper.args import args_shift_one

if TYPE_CHECKING:
    from src.core.response.QueuedCollectionResponse import (
        QueuedCollectionResponse,
        QueuedCollectionStepsList,
    )


class QueuedCollectionPathManager(HasResponse, HasRequest):
    def __init__(self, root_request) -> None:
        HasResponse.__init__(self)
        HasRequest.__init__(self)

        self.root_request = root_request
        self._response: Optional["QueuedCollectionResponse"] = None
        self.steps: "QueuedCollectionStepsList" = [None]
        self.map = {}

        args = root_request.args
        steps = args_shift_one(args, "command-request-step")
        if steps:
            self.steps: "QueuedCollectionStepsList" = list(
                map(int, str(steps).split("."))
            )

    def get_response(self) -> "QueuedCollectionResponse":
        return cast("QueuedCollectionResponse", super().get_response())

    def get_step_index(self) -> int:
        return self.steps[self.get_response().step_position]

    def start_rendering(
        self, request: CommandRequest, response: AbstractResponse
    ) -> None:
        self.set_request(request)
        self.set_response(response)

        # Assign position
        if response.parent:
            response.step_position = (
                self.get_response().find_parent_response_collection().step_position + 1
            )

    def save_to_map(self) -> None:
        response = self.get_response()

        response.kernel.io.log(
            f"Command: {self.get_request().get_string_command()}",
            verbosity=VERBOSITY_LEVEL_MAXIMUM,
        )
        response.kernel.io.log(
            f"  Step path: {self.build_step_path()}", verbosity=VERBOSITY_LEVEL_MAXIMUM
        )
        response.kernel.io.log(
            f"  Step position: {response.step_position}",
            verbosity=VERBOSITY_LEVEL_MAXIMUM,
        )
        response.kernel.io.log(
            f"  Step index: {self.get_step_index()}", verbosity=VERBOSITY_LEVEL_MAXIMUM
        )

        self.map[self.build_step_path()] = response

    def has_child_queue(self) -> bool:
        return self.get_response().step_position >= len(self.steps)

    def build_step_path(self, steps: Optional[QueuedCollectionStepsList] = None) -> str:
        return ".".join(map(str, steps if steps is not None else self.steps))
