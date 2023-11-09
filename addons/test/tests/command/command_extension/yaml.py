from tests.AbstractTestCase import AbstractTestCase


class TestTestCommandCommandExtensionYaml(AbstractTestCase):
    def test_yaml(self):
        response = self.kernel.run_command('test::command-extension/yaml')

        self.assertIsNone(
            response.first()
        )
