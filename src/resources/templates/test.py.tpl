from addons.{addon_name}.command.{dir_group}.{dir_name} import {command_function_name}
from tests.AbstractTestCase import AbstractTestCase


class {class_name}(AbstractTestCase):
    def {method_name}(self):
        # TO/DO
        response = self.kernel.run_function({command_function_name}, {{
            'option': 'test'
        }})

        self.assertEqual(
            response.first(),
            'something'
        )
