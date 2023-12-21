from __future__ import annotations

import os
from typing import TYPE_CHECKING, List, Optional, cast

from src.const.globals import KERNEL_RENDER_MODE_TERMINAL
from src.const.types import (
    AnyCallable,
    BasicValue,
    CoreCommandArgsDict,
    OptionalCoreCommandArgsDict,
    ResponsePrintType,
)
from src.core.command.resolver.AbstractCommandResolver import AbstractCommandResolver
from src.core.CommandRequest import CommandRequest
from src.core.response.AbortResponse import AbortResponse
from src.core.response.AbstractResponse import AbstractResponse
from src.core.response.FunctionResponse import FunctionResponse
from src.core.response.queue_collection.DefaultQueuedCollectionResponseQueueManager import (
    DefaultQueuedCollectionResponseQueueManager,
)
from src.core.response.queue_collection.FastModeQueuedCollectionResponseQueueManager import (
    FastModeQueuedCollectionResponseQueueManager,
)
from src.core.response.queue_collection.QueuedCollectionPathManager import (
    QueuedCollectionPathManager,
)
from src.core.response.queue_collection.QueuedCollectionStopCurrentStepResponse import (
    QueuedCollectionStopCurrentStepResponse,
)
from src.core.response.queue_collection.QueuedCollectionStopResponse import (
    QueuedCollectionStopResponse,
)
from src.helper.args import args_in_function, args_is_basic_value

if TYPE_CHECKING:
    from src.core.Kernel import Kernel

QueuedCollectionStepValue = int | None
QueuedCollectionStepsList = List[QueuedCollectionStepValue]
QueuedCollectionResponseCollection = List[BasicValue | AnyCallable | AbstractResponse]


class QueuedCollectionResponse(AbstractResponse):
    ids_counter = 0

    def __init__(
        self, kernel: "Kernel", collection: QueuedCollectionResponseCollection
    ) -> None:
        super().__init__(kernel)
        self.collection: QueuedCollectionResponseCollection = collection
        self.step_position: int = 0
        self._path_manager: Optional[QueuedCollectionPathManager] = None

        manager_class = (
            FastModeQueuedCollectionResponseQueueManager
            if self.kernel.fast_mode
            else DefaultQueuedCollectionResponseQueueManager
        )
        self.queue_manager = manager_class(self)

        # For debug purpose
        self.id = QueuedCollectionResponse.ids_counter
        QueuedCollectionResponse.ids_counter += 1

    def set_path_manager(self, path_manager: QueuedCollectionPathManager) -> None:
        self._path_manager = path_manager

    def get_path_manager(self) -> QueuedCollectionPathManager:
        self._validate__should_not_be_none(self._path_manager)
        assert self._path_manager is not None

        return self._path_manager

    def find_parent_response_collection(self) -> "None|QueuedCollectionResponse":
        current: Optional["AbstractResponse"] = self
        while current is not None:
            current = current.parent
            if isinstance(current, QueuedCollectionResponse):
                return current

        return None

    def init_path_manager(self, request: CommandRequest) -> QueuedCollectionPathManager:
        # Share path manager across root request and all involved collections
        root_request = request.get_root_parent()
        if "queue_collection_path_manager" not in root_request.storage:
            root_request.storage[
                "queue_collection_path_manager"
            ] = QueuedCollectionPathManager(root_request)

        path_manager = root_request.storage["queue_collection_path_manager"]
        self.set_path_manager(path_manager)

        return cast(QueuedCollectionPathManager, path_manager)

    def render_content(
        self,
        request: CommandRequest,
        render_mode: str = KERNEL_RENDER_MODE_TERMINAL,
        args: OptionalCoreCommandArgsDict = None,
    ) -> AbstractResponse:
        if not request.resolver:
            return AbortResponse(
                kernel=self.kernel, reason="MISSING_REQUEST_INITIALIZATION"
            )

        resolver: AbstractCommandResolver = request.resolver
        path_manager = self.init_path_manager(request)
        path_manager.start_rendering(request, self)

        # Collection is empty, nothing to do
        if not len(self.collection):
            return self.queue_manager.render_content_complete()

        # There is a deeper level.
        if path_manager.has_child_queue():
            # Append a new step level,
            # set to None to postpone processing
            path_manager.steps.append(None)

        step_index = path_manager.get_step_index()
        path_manager.save_to_map()

        # First time, do not execute, wait next iteration
        if step_index is None:
            self.queue_manager.enqueue_next_step_by_index(0)

            return self.queue_manager.render_content_complete()

        # Prepare args
        render_args = cast(CoreCommandArgsDict, {"queue": self.queue_manager})

        # Transform item in a response object.
        response = resolver.wrap_response(self.collection[step_index])

        if isinstance(response, FunctionResponse):
            if not args_in_function(response.function, "queue"):
                raise self.kernel.io.error(
                    'Argument "queue: AbstractQueuedCollectionResponseQueueManager" '
                    "is required by every callback function in queue collection response, in : "
                    + str(response.function)
                )

        response.render(request=request, args=render_args, render_mode=render_mode)

        first_response_item = None
        if len(response.output_bag) >= 1:
            first_response_item = response.output_bag[0]

        # If first item is of type "response"
        # the base response is probably a function
        # which have been executed and returning a new response
        if isinstance(first_response_item, AbstractResponse):
            response = first_response_item

        # Support simple abort response, which is an alias of a stop response.
        if isinstance(response, AbortResponse):
            response = QueuedCollectionStopResponse(self.kernel, response.reason)

        self.output_bag.append(response)

        # Response asks to stop all process
        if isinstance(response, QueuedCollectionStopResponse) or isinstance(
            response, QueuedCollectionStopCurrentStepResponse
        ):
            if isinstance(response, QueuedCollectionStopResponse):
                # Mark having next step to block enqueuing
                self.has_next_step = True

            return self.queue_manager.render_content_complete()

        if isinstance(response, QueuedCollectionResponse):
            if response.has_next_step:
                self.has_next_step = response.has_next_step
                return self.queue_manager.render_content_complete()

        if not isinstance(response, AbstractResponse) and not args_is_basic_value(
            response
        ):
            self.kernel.io.error(
                f"Returned data and nested values should be simple data : int, string, list or dict"
            )

        self.queue_manager.enqueue_next_step_if_exists(step_index, response)

        return self.queue_manager.render_content_complete()

    def print(
        self,
        render_mode: str = KERNEL_RENDER_MODE_TERMINAL,
        interactive_data: bool = True,
    ) -> ResponsePrintType:
        output = super().print(render_mode, interactive_data)

        if isinstance(output, list) and len(output):
            return os.linesep.join(map(str, output))

        return output
