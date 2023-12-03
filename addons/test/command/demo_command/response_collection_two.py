from typing import TYPE_CHECKING

from addons.core.command.check.hi import core__check__hi
from addons.test.command.demo_command.response_collection_three import (
    test__demo_command__response_collection_three,
)
from src.core.response.AbstractResponse import AbstractResponse
from src.core.response.InteractiveShellCommandResponse import (
    InteractiveShellCommandResponse,
)
from src.core.response.queue_collection.AbstractQueuedCollectionResponseQueueManager import (
    AbstractQueuedCollectionResponseQueueManager,
)
from src.core.response.QueuedCollectionResponse import QueuedCollectionResponse
from src.decorator.option import option
from src.decorator.test_command import test_command

if TYPE_CHECKING:
    from src.core.Kernel import Kernel

TEST_DEMO_COMMAND_TWO_RESULT_FIRST = "..TWO:simple-text"
TEST_DEMO_COMMAND_TWO_RESULT_SHELL = "..TWO:shell-response"


@test_command()
@option("--abort", "-a", is_flag=True, required=False, help="Ask to abort")
def test__demo_command__response_collection_two(
    kernel: "Kernel", abort: bool = False
) -> QueuedCollectionResponse:
    def _test__demo_command__response_collection_two__simple_function(
        queue: AbstractQueuedCollectionResponseQueueManager,
    ) -> str:
        return f"..TWO:simple-function-previous-value:should-be-string={queue.get_previous_value()}"

    def _test__demo_command__response_collection_two__another_simple_function(
        queue: AbstractQueuedCollectionResponseQueueManager,
    ) -> str:
        return f"..TWO:another-simple-function-previous-value:should-be-none={queue.get_previous_value()}"

    def _test__demo_command__response_collection_two__run_another_collection(
        queue: AbstractQueuedCollectionResponseQueueManager,
    ) -> AbstractResponse:
        nonlocal abort

        # This run will return unused response.
        kernel.run_function(
            core__check__hi,
        )

        return kernel.run_function(
            test__demo_command__response_collection_three, {"abort": abort}
        )

    def _test__demo_command__response_collection_three_command(
        queue: AbstractQueuedCollectionResponseQueueManager,
    ) -> InteractiveShellCommandResponse:
        return InteractiveShellCommandResponse(
            kernel, ["echo", "..TWO:interactive-shell-response"]
        )

    return QueuedCollectionResponse(
        kernel,
        [
            TEST_DEMO_COMMAND_TWO_RESULT_FIRST,
            f"{TEST_DEMO_COMMAND_TWO_RESULT_FIRST}(2)",
            _test__demo_command__response_collection_two__simple_function,
            InteractiveShellCommandResponse(
                kernel, ["echo", f'"{TEST_DEMO_COMMAND_TWO_RESULT_SHELL}"']
            ),
            _test__demo_command__response_collection_two__another_simple_function,
            _test__demo_command__response_collection_two__run_another_collection,
            _test__demo_command__response_collection_three_command,
        ],
    )
