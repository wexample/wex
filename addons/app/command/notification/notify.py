from src.const.globals import COMMAND_TYPE_ADDON
from addons.app.decorator.app_command import app_command
from src.decorator.option import option
from addons.app.AppAddonManager import AppAddonManager
from src.const.globals import COMMAND_CHAR_SERVICE, COMMAND_SEPARATOR_ADDON


@app_command(help="Description", command_type=COMMAND_TYPE_ADDON)
@option('--action', '-a', type=str, required=True, help="Action name")
def app__notification__notify(manager: AppAddonManager, app_dir: str, action: str) -> None:
    notification_service = manager.get_config("notification.service").get_str()

    manager.kernel.run_command(
        f"{COMMAND_CHAR_SERVICE}{notification_service}{COMMAND_SEPARATOR_ADDON}notification/notify",
        {
            "action": action
        }
    )
