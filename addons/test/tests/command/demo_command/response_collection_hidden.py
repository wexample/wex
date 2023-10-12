from addons.test.command.demo_command.response_collection_hidden import test__demo_command__response_collection_hidden
from src.core.response.ResponseCollectionHiddenResponse import ResponseCollectionHiddenResponse
from tests.AbstractTestCase import AbstractTestCase


class TestTestCommandDemoCommandResponseCollectionHidden(AbstractTestCase):
    def test_response_collection_hidden(self):
        response = self.kernel.run_function(
            test__demo_command__response_collection_hidden
        )

        self.assertTrue(
            isinstance(
                response.output_bag[0],
                ResponseCollectionHiddenResponse
            ),
            'The first response is hidden'
        )

        self.assertEqual(
            response.output_bag[0].print(
                interactive_data=False
            ),
            'simple-text',
            'The first response value can be reached'
        )

        self.assertIsNone(
            response.output_bag[0].print(),
            'The first response is not rendered in normal mode'
        )

        self.assertEqual(
            response.output_bag[1].first(),
            'simple-text-has-been-passed',
            'The response has been passed to second function'
        )

        self.assertEqual(
            response.print(),
            'simple-text-has-been-passed',
            'Only the second function response is returned'
        )
