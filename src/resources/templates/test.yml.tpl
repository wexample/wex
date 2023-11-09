from tests.AbstractTestCase import AbstractTestCase


class {class_name}(AbstractTestCase):
    def {method_name}(self):
        # TO/DO
        response = self.kernel.run_command('{command}', {{
            'arg': 'test'
        }})

        self.assertEqual(
            response.first(),
            'something'
        )
