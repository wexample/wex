from tests.AbstractTestCase import AbstractTestCase


class TestTestCommandAppYaml(AbstractTestCase):
    def test_yaml(self):
        response = self.kernel.run_command('test::app/yaml', {
            'option': 'test'
        })

        self.assertEqual(
            response.output_bag[0].print(),
            'Inline bash script example'
        )

