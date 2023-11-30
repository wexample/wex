from typing import TYPE_CHECKING, Any, Dict

from addons.test.command.demo_command.counting_collection import (
    test__demo_command__counting_collection,
)
from addons.test.command.demo_command.response_collection_two import (
    test__demo_command__response_collection_two,
)
from src.const.types import StringKeysDict
from src.core.response.AbstractResponse import AbstractResponse
from src.core.response.HiddenResponse import HiddenResponse
from src.core.response.NonInteractiveShellCommandResponse import (
    NonInteractiveShellCommandResponse,
)
from src.core.response.queue_collection.AbstractQueuedCollectionResponseQueueManager import (
    AbstractQueuedCollectionResponseQueueManager,
)
from src.core.response.QueuedCollectionResponse import QueuedCollectionResponse
from src.decorator.option import option
from src.decorator.test_command import test_command

if TYPE_CHECKING:
    from src.core.Kernel import Kernel

TEST_DEMO_COMMAND_RESULT_FIRST_FUNCTION = "function-response-text"


@test_command()
@option("--abort", "-a", is_flag=True, required=False, help="Ask to abort")
def test__demo_command__response_collection(
    kernel: "Kernel", abort: bool = False
) -> QueuedCollectionResponse:
    def _test__demo_command__response_collection__first_function(
        queue: AbstractQueuedCollectionResponseQueueManager,
    ) -> str:
        return TEST_DEMO_COMMAND_RESULT_FIRST_FUNCTION

    def _test__demo_command__response_collection__second_function(
        queue: AbstractQueuedCollectionResponseQueueManager,
    ) -> StringKeysDict:
        return {"old": queue.get_previous_value(), "new": "two"}

    def _test__demo_command__response_collection__function_three(
        queue: AbstractQueuedCollectionResponseQueueManager,
    ) -> StringKeysDict:
        previous = queue.get_previous_value()
        return {"type": str(type(previous)), "length": len(previous)}

    def _test__demo_command__response_collection__sub_function_shell(
        queue: AbstractQueuedCollectionResponseQueueManager,
    ) -> NonInteractiveShellCommandResponse:
        previous = queue.get_previous_value()
        assert isinstance(previous, list)

        return NonInteractiveShellCommandResponse(
            kernel, ["echo", "--sub-function-shell:" + previous[0]]
        )

    def _test__demo_command__response_collection__callback_hidden_response(
        queue: AbstractQueuedCollectionResponseQueueManager,
    ) -> HiddenResponse:
        previous = queue.get_previous_value()
        assert isinstance(previous, str)

        return HiddenResponse(kernel, previous + "-has-been-passed-to-hidden")

    def _test__demo_command__response_collection__previous(
        queue: AbstractQueuedCollectionResponseQueueManager,
    ) -> str:
        return str(queue.get_previous_value()) + "-and-returned-by-next"

    def _test__demo_command__response_collection__sub_collection(
        queue: AbstractQueuedCollectionResponseQueueManager,
    ) -> QueuedCollectionResponse:
        previous = queue.get_previous_value()

        def callback() -> Dict[str, Any]:
            return {"passed": previous}

        return QueuedCollectionResponse(
            kernel,
            [
                "--sub-collection-in-function:simple-text",
                "--sub-collection-in-function:simple-text-2",
                45600,
                456.00,
                # Will be converted to FunctionResponse
                _test__demo_command__response_collection__first_function,
                NonInteractiveShellCommandResponse(
                    kernel, ["echo", "--sub-collection-shell:simple-text"]
                ),
                callback,
            ],
        )

    def _test__demo_command__response_collection__run_another_collection(
        queue: AbstractQueuedCollectionResponseQueueManager,
    ) -> AbstractResponse:
        nonlocal abort

        return kernel.run_function(
            test__demo_command__response_collection_two, {"abort": abort}
        )

    def _test__demo_command__response_collection__counting_collection(
        queue: AbstractQueuedCollectionResponseQueueManager,
    ) -> AbstractResponse:
        previous = queue.get_previous_value()
        kernel.io.log("Previous : " + str(previous))

        error = False
        if previous != "__previous__":
            error: True

        response = kernel.run_function(
            test__demo_command__counting_collection, {"initial": 1000}
        )

        rendered = response.print()

        if error:
            kernel.io.error(
                f"Bad previous to response match : previous : {previous}, rendered : {rendered}"
            )
        return response

    return QueuedCollectionResponse(
        kernel,
        [
            "simple-response-text",
            "simple-response-text-2",
            123456,
            123.456,
            ["simple-list", "simple-list"],
            {"simple-dict": True},
            # Will be converted to FunctionResponse
            _test__demo_command__response_collection__first_function,
            _test__demo_command__response_collection__second_function,
            _test__demo_command__response_collection__function_three,
            NonInteractiveShellCommandResponse(kernel, ["echo", "shell-text"]),
            _test__demo_command__response_collection__sub_function_shell,
            "free-text-after-shell",
            _test__demo_command__response_collection__callback_hidden_response,
            _test__demo_command__response_collection__previous,
            QueuedCollectionResponse(
                kernel,
                [
                    "--sub-collection-direct:simple-text",
                ],
            ),
            _test__demo_command__response_collection__run_another_collection,
            _test__demo_command__response_collection__run_another_collection,
            _test__demo_command__response_collection__sub_collection,
            _test__demo_command__response_collection__sub_collection,
            "__previous__",
            _test__demo_command__response_collection__counting_collection,
            _test__demo_command__response_collection__counting_collection,
            "last-text",
        ],
    )
