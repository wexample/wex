from src.core.Kernel import Kernel
from src.decorator.test_command import test_command
from addons.app.decorator.app_webhook import app_webhook
from src.const.globals import COMMAND_TYPE_SERVICE


@app_webhook()
@test_command(command_type=COMMAND_TYPE_SERVICE)
def test__webhook__test_command(kernel: Kernel, service: str):
    return 'TEST_WEBHOOK_COMMAND'
