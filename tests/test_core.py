from AbstractTestCase import AbstractTestCase


class TestCore(AbstractTestCase):
    def test_core_action(self):
        self.assertEqual(
            self.kernel.exec('hi'),
            'hi!'
        )

        self.assertTrue(False)
