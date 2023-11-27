from addons.test.command.template.log import test__template__log
from tests.AbstractTestCase import AbstractTestCase


class TestTestCommandTemplateLog(AbstractTestCase):
    def test_log(self):
        response = self.kernel.run_function(test__template__log)

        self.assertEqual(response.print(), "COMPLETE")
