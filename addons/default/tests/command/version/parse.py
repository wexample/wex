from addons.default.command.version.parse import default__version__parse
from addons.default.const.default import UPGRADE_TYPE_BETA
from tests.AbstractTestCase import AbstractTestCase


class TestDefaultCommandVersionParse(AbstractTestCase):
    def test_parse(self):
        result = self.kernel.run_function(default__version__parse, {
            'version': '5.0.0-beta.41+build.20230822134237'
        })

        self.assertDictKeysEquals({
            'major': '5',
            'intermediate': '0',
            'minor': '0',
            'pre_build_type': UPGRADE_TYPE_BETA,
            'pre_build_number': '41',
            'build_metadata': '20230822134237'
        }, result)
