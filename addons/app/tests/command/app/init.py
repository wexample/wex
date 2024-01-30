from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase


class TestAppCommandAppInit(AbstractAppTestCase):
    def test_init(self) -> None:
        # Test without any service
        self.create_test_app(force_restart=True)

        # Test with a service
        self.create_and_start_test_app(services=["php"], force_restart=True)
