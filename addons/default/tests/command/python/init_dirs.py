from addons.default.command.python.init_dirs import default__python__init_dirs
from tests.AbstractTestCase import AbstractTestCase


class TestDefaultCommandPythonInitDirs(AbstractTestCase):
    def test_init_dirs(self) -> None:
        # TODO
        response = self.kernel.run_function(default__python__init_dirs, {
            'option': 'test'
        })

        self.assertEqual(
            response.first(),
            'something'
        )
