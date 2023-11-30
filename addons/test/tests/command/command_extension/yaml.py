from tests.AbstractTestCase import AbstractTestCase


class TestTestCommandCommandExtensionYaml(AbstractTestCase):
    def test_yaml(self) -> None:
        response = self.kernel.run_command(
            "test::command-extension/yaml", {"test-option": "THIS_IS_A_TEST"}
        )

        self.assertResponseOutputBagItemContains(response, 1, "THIS_IS_A_TEST")

        self.assertResponseOutputBagItemContains(
            response, 3, "SIMPLE_SHELL_FILE_RESPONSE"
        )
        self.assertResponseOutputBagItemContains(response, 4, "simple quotes")
        self.assertResponseOutputBagItemContains(response, 5, "double quotes")
        self.assertResponseOutputBagItemContains(response, 6, "simple quotes")
        self.assertResponseOutputBagItemContains(response, 6, "double quotes")
        self.assertResponseOutputBagItemContains(
            response, 7, "SIMPLE_PYTHON_FILE_RESPONSE"
        )
