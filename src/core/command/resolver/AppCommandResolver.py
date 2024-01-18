import os
from typing import TYPE_CHECKING, Optional, cast

from addons.app.const.app import APP_DIR_APP_DATA, ERR_APP_NOT_FOUND
from src.const.globals import (
    COMMAND_CHAR_APP,
    COMMAND_PATTERN_APP,
    COMMAND_SEPARATOR_GROUP,
    COMMAND_TYPE_APP,
)
from src.const.types import RegistryCommandsCollection, StringsList
from src.core.command.resolver.AbstractCommandResolver import AbstractCommandResolver
from src.core.CommandRequest import CommandRequest
from src.core.response.AbortResponse import AbortResponse
from src.core.response.AbstractResponse import AbstractResponse
from src.core.response.queue_collection.QueuedCollectionStopResponse import (
    QueuedCollectionStopResponse,
)
from src.helper.string import string_to_kebab_case, string_to_snake_case

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


class AppCommandResolver(AbstractCommandResolver):
    def __init__(self, kernel: "Kernel") -> None:
        from addons.app.AppAddonManager import AppAddonManager

        super().__init__(kernel)

        # Shortcut.
        self.app_addon_manager: "AppAddonManager" = cast(
            AppAddonManager, kernel.addons["app"]
        )

    def render_request(
        self, request: CommandRequest, render_mode: str
    ) -> AbstractResponse:
        if not self.get_base_path():
            if not request.quiet:
                self.kernel.io.error(
                    ERR_APP_NOT_FOUND,
                    {
                        "command": request.get_string_command(),
                        "dir": os.getcwd(),
                    },
                )

            return AbortResponse(self.kernel, reason=ERR_APP_NOT_FOUND)

        return super().render_request(request, render_mode)

    @classmethod
    def get_pattern(cls) -> str:
        return COMMAND_PATTERN_APP

    @classmethod
    def get_type(cls) -> str:
        return COMMAND_TYPE_APP

    def build_path(
        self, request: CommandRequest, extension: str, subdir: Optional[str] = None
    ) -> Optional[str]:
        match = request.get_match()
        base_path = self.get_base_path()
        if not base_path:
            return None

        return self.build_command_path(
            base_path=base_path,
            extension=extension,
            subdir=subdir,
            command_path=os.path.join(
                string_to_snake_case(match[2]),
                string_to_snake_case(match[3]),
            ),
        )

    def build_command_from_parts(self, parts: StringsList) -> str:
        # Convert each part to kebab-case
        kebab_parts = [string_to_kebab_case(part) for part in parts]

        return f"{COMMAND_CHAR_APP}{kebab_parts[1]}{COMMAND_SEPARATOR_GROUP}{kebab_parts[2]}"

    def get_function_name_parts(self, parts: StringsList) -> StringsList:
        return ["app", parts[1], parts[2]]

    def get_base_path(self) -> Optional[str]:
        app_dir = self.app_addon_manager.app_dir
        if not app_dir:
            from addons.app.command.location.find import _app__location__find

            app_dir = _app__location__find(
                manager=self.app_addon_manager,
                app_dir=os.getcwd() + os.sep,
            )

        if app_dir:
            return f"{app_dir}{APP_DIR_APP_DATA}"

        return None

    def autocomplete_suggest(
        self, cursor: int, search_split: StringsList
    ) -> str | None:
        if cursor == 0:
            # User typed "."
            if search_split[0].startswith(COMMAND_CHAR_APP):
                app_path = self.get_base_command_path()

                # We are in an app dir or subdir
                if app_path:
                    return " ".join(
                        self.suggest_from_path(
                            app_path,
                            search_split[0],
                        )
                    )

            elif search_split[0] == "":
                # We are in an app dir or subdir
                if self.get_base_command_path():
                    # Suggest to execute local app command
                    return COMMAND_CHAR_APP

        # Arguments
        elif cursor >= 1:
            if search_split[0].startswith(COMMAND_CHAR_APP):
                return self.suggest_arguments(
                    search_split[0],
                    search_split[cursor],
                )

        return None

    def build_command_parts_from_url_path_parts(
        self, path_parts: StringsList
    ) -> StringsList:
        return [
            COMMAND_CHAR_APP,
            path_parts[2],
            path_parts[3],
        ]

    def run_command_request_from_url_path(self, path: str) -> AbstractResponse:
        from src.core.response.AbortResponse import AbortResponse
        from src.helper.string import string_to_snake_case

        parts = path.split("/")

        internal_command = self.create_command_from_path(path)

        if not internal_command:
            return AbortResponse(kernel=self.kernel, reason="WEBHOOK_COMMAND_NOT_FOUND")

        environment = string_to_snake_case(parts[0])
        app_name = string_to_snake_case(parts[1])
        apps = self.app_addon_manager.get_proxy_apps(environment)

        if app_name not in apps:
            return AbortResponse(kernel=self.kernel, reason="WEBHOOK_APP_NOT_FOUND")

        self_super: AbstractCommandResolver = cast(AbstractCommandResolver, super())

        def _callback() -> AbstractResponse:
            request = self.kernel.create_command_request(internal_command)

            if not request._script_command:
                return AbortResponse(
                    kernel=self.kernel, reason="WEBHOOK_REQUEST_NOT_FOUND"
                )

            # Hooking this command is not allowed
            if not request.get_script_command().get_extra_value("app_webhook", False):
                return QueuedCollectionStopResponse(
                    self.kernel, "Function is not a webhook"
                )

            return self_super.run_command_request_from_url_path(path)

        response = self.app_addon_manager.exec_in_app_workdir(apps[app_name], _callback)
        assert isinstance(response, AbstractResponse)

        return response

    def get_active_commands(self) -> RegistryCommandsCollection:
        # Use ap dir if specified.
        app_dir = self.app_addon_manager.app_dir

        if not app_dir:
            # Search commands from current working dir, ignoring if initial command is an app command.
            app_dir = self.kernel.get_path("call")

        app_command_dir = self.build_base_command_path(
            os.path.join(app_dir, APP_DIR_APP_DATA)
        )

        return self.scan_commands_groups(app_command_dir)
