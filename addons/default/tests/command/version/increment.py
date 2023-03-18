from tests.AbstractTestCase import AbstractTestCase


class TestDefaultCommandVersionIncrement(AbstractTestCase):
    def test_increment(self):
        version = self.kernel.exec(
            'default::version/increment',
            {
                'version': '1.0.0',
            }
        )

        self.assertTrue(version and version.startswith('1.0.1'))
