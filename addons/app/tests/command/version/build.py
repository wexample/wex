from addons.app.command.config.get import app__config__get
from addons.app.command.version.build import app__version__build
from tests.AbstractTestCase import AbstractTestCase


class TestAppCommandVersionBuild(AbstractTestCase):
    def test_build(self):
        current_version = self.kernel.exec_function(
            app__config__get,
            {
                'key': 'global.version'
            }
        )

        # Change version.
        version = self.kernel.exec_function(
            app__version__build,
            {
                'version': '1.0.0'
            }
        )

        self.assertEqual(version, '1.0.0')

        # Rollback.
        self.kernel.exec_function(
            app__version__build,
            {
                'version': current_version
            }
        )
