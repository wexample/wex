from src.core.response.ResponseCollectionHiddenResponse import ResponseCollectionHiddenResponse
from src.core.response.ResponseCollectionResponse import ResponseCollectionResponse
from src.decorator.command import command
from src.core import Kernel


@command(help="Test returning value which should not be printed to user")
def test__demo_command__response_collection_hidden(kernel: Kernel):
    def _callback(previous):
        return previous + '-has-been-passed'

    return ResponseCollectionResponse(
        kernel,
        [
            ResponseCollectionHiddenResponse(
                kernel,
                'simple-text'
            ),
            _callback
        ]
    )
