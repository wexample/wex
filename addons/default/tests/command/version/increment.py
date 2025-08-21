from addons.default.command.version.increment import \
    default__version__increment
from src.const.globals import VERSION_DEFAULT
from tests.AbstractTestCase import AbstractTestCase


class TestDefaultCommandVersionIncrement(AbstractTestCase):
    def test_increment(self) -> None:
        version = self.kernel.run_function(
            default__version__increment,
            {
                "version": VERSION_DEFAULT,
            },
        ).first()

        self.assertTrue(version and version.startswith("1.0.1"))
