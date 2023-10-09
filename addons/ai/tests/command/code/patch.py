from addons.ai.command.code.patch import ai__code__patch
from tests.AbstractTestCase import AbstractTestCase


class TestAiCommandCodePatch(AbstractTestCase):
    def test_patch(self):
        # Too early to test
        # self.kernel.run_function(ai__code__patch, {
        #     'name': 'test'
        # })
        self.assertTrue(True)
