from addons.test.command.demo_command.responses import test__demo_command__responses, RESPONSES_DEFAULT_VALUES
from tests.AbstractTestCase import AbstractTestCase


class TestTestCommandDemoCommandResponses(AbstractTestCase):
    def test_responses(self):
        for type in RESPONSES_DEFAULT_VALUES:
            response = self.kernel.run_function(
                test__demo_command__responses,
                {
                    'type': type
                }
            )

            self.assertEqual(
                response,
                RESPONSES_DEFAULT_VALUES[type]
            )

        # TODO
        # Python function
        response = self.kernel.run_function(
            test__demo_command__responses,
            {
                'type': 'function'
            }
        )

        self.assertEqual(
            response,
            'one'
        )
        #
        # # Shell script
        # response = self.kernel.run_function(
        #     test__demo_command__responses,
        #     {
        #         'type': 'shell'
        #     }
        # )
        #
        # self.assertEqual(
        #     response,
        #     'one'
        # )
