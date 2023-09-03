from addons.default.command.version.increment import default__version__increment
from tests.AbstractTestCase import AbstractTestCase


class TestDefaultCommandVersionIncrement(AbstractTestCase):
    def test_increment(self):
        version = self.kernel.run(
            default__version__increment,
            {
                'version': '1.0.0',
            }
        )

        self.assertTrue(version and version.startswith('1.0.1'))
