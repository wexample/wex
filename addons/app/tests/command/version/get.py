import os

from addons.app.command.version.get import app__version__get
from addons.default.helper.migration import MIGRATION_MINIMAL_VERSION
from src.const.globals import SYSTEM_WWW_PATH
from src.helper.core import core_kernel_get_version
from tests.AbstractTestCase import AbstractTestCase


class TestAppCommandVersionGet(AbstractTestCase):
    def test_get(self):
        self.log('Test in ' + SYSTEM_WWW_PATH)

        version = self.kernel.run_function(
            app__version__get, {
                'app-dir': SYSTEM_WWW_PATH
            })

        self.assertEquals(
            version.print(),
            MIGRATION_MINIMAL_VERSION
        )

        self.log('Test in ' + os.getcwd())

        version = self.kernel.run_function(app__version__get)

        self.assertEquals(
            version.print(),
            core_kernel_get_version(self.kernel)
        )
