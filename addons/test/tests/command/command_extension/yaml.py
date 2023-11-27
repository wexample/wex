from tests.AbstractTestCase import AbstractTestCase


class TestTestCommandCommandExtensionYaml(AbstractTestCase):
    def test_yaml(self):
        response = self.kernel.run_command(
            "test::command-extension/yaml", {"test-option": "THIS_IS_A_TEST"}
        )

        self.assertTrue("THIS_IS_A_TEST" in response.output_bag[1].print())

        self.assertTrue(response.output_bag[3].first(), "SIMPLE_SHELL_FILE_RESPONSE")

        self.assertTrue(
            "simple quotes" in response.output_bag[4].print(),
        )

        self.assertTrue(
            "double quotes" in response.output_bag[5].print(),
        )

        self.assertTrue(
            "simple quotes" in response.output_bag[6].print()
            and "double quotes" in response.output_bag[6].print(),
        )

        self.assertTrue(response.output_bag[7].first(), "SIMPLE_PYTHON_FILE_RESPONSE")
