from __future__ import annotations

from src.const.globals import VERBOSITY_LEVEL_MAXIMUM
from src.core.CommandRequest import CommandRequest
from src.core.response.AbstractResponse import AbstractResponse
from src.helper.args import args_shift_one


class QueuedCollectionPathManager:
    def __init__(self, root_request) -> None:
        self.root_request = root_request
        self.response = None
        self.request = None
        self.steps = [None]
        self.map = {}

        args = root_request.args
        steps = args_shift_one(args, "command-request-step")
        if steps:
            self.steps = list(map(int, str(steps).split(".")))

    def get_step_index(self) -> int:
        return self.steps[self.response.step_position]

    def start_rendering(
        self, request: CommandRequest, response: AbstractResponse
    ) -> None:
        self.request = request
        self.response = response

        # Assign position
        if self.response.parent:
            self.response.step_position = (
                self.response.find_parent_response_collection().step_position + 1
            )

    def save_to_map(self) -> None:
        self.response.kernel.io.log(
            f"Command: {self.request.string_command}", verbosity=VERBOSITY_LEVEL_MAXIMUM
        )
        self.response.kernel.io.log(
            f"  Step path: {self.build_step_path()}", verbosity=VERBOSITY_LEVEL_MAXIMUM
        )
        self.response.kernel.io.log(
            f"  Step position: {self.response.step_position}",
            verbosity=VERBOSITY_LEVEL_MAXIMUM,
        )
        self.response.kernel.io.log(
            f"  Step index: {self.get_step_index()}", verbosity=VERBOSITY_LEVEL_MAXIMUM
        )

        self.map[self.build_step_path()] = self.response

    def has_child_queue(self) -> bool:
        return self.response.step_position >= len(self.steps)

    def build_step_path(self, steps=None) -> str:
        return ".".join(map(str, steps if steps is not None else self.steps))
