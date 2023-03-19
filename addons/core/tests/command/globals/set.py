import importlib
import re

from src.const.globals import WEX_VERSION, PATH_GLOBALS

from tests.AbstractTestCase import AbstractTestCase


class TestCoreCommandGlobalsSet(AbstractTestCase):
    def check_version(self, expected):
        with open(PATH_GLOBALS, "r") as file:
            content = file.read()

        pattern = r"WEX_VERSION\s*=\s*'([^']+)'"
        match = re.search(pattern, content)

        self.assertIsNotNone(match)

        self.assertEqual(
            match.group(1),
            expected
        )

    def test_set(self):
        original_version = WEX_VERSION

        # Change value.
        self.kernel.exec('core::globals/set', {
            'key': 'WEX_VERSION',
            'value': 'wex-test-version',
            'verbose': True
        })

        self.check_version('wex-test-version')

        self.kernel.exec('core::globals/set', {
            'key': 'WEX_VERSION',
            'value': original_version,
            'verbose': True
        })

        self.check_version(original_version)
