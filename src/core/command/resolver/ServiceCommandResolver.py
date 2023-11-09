import os

from addons.app.const.app import ERR_SERVICE_NOT_FOUND
from src.core.CommandRequest import CommandRequest
from src.core.response.AbstractResponse import AbstractResponse
from src.core.response.AbortResponse import AbortResponse
from src.helper.string import to_snake_case
from src.const.globals import COMMAND_PATTERN_SERVICE, COMMAND_TYPE_SERVICE, \
    COMMAND_CHAR_SERVICE, COMMAND_SEPARATOR_ADDON
from src.core.command.resolver.AbstractCommandResolver import AbstractCommandResolver


class ServiceCommandResolver(AbstractCommandResolver):
    def render_request(self, request: CommandRequest, render_mode: str) -> AbstractResponse:
        service = to_snake_case(request.match[1])
        if service not in self.kernel.registry['service']:
            if not request.quiet:
                self.kernel.io.error(ERR_SERVICE_NOT_FOUND, {
                    'command': request.command,
                    'service': service,
                })
            return AbortResponse(self.kernel, reason=ERR_SERVICE_NOT_FOUND)

        # Guess service name from command prefix if not passed.
        if '--service' not in request.args:
            request.args.extend([
                '--service',
                request.match[1]
            ])

        return super().render_request(request, render_mode)

    @classmethod
    def get_pattern(cls) -> str:
        return COMMAND_PATTERN_SERVICE

    @classmethod
    def get_type(cls) -> str:
        return COMMAND_TYPE_SERVICE

    def build_command_from_parts(self, parts: list) -> str:
        return COMMAND_CHAR_SERVICE + super().build_command_from_parts(parts)

    def build_path(self, request: CommandRequest, extension: str, subdir: str = None) -> str | None:
        return self.build_command_path(
            base_path=f"{self.kernel.registry['service'][to_snake_case(request.match[1])]['dir']}",
            extension=extension,
            subdir=subdir,
            command_path=os.path.join(to_snake_case(request.match.group(2)), to_snake_case(request.match.group(3)))
        )

    def get_function_name_parts(self, parts: list) -> []:
        return [
            parts[0],
            parts[1],
            parts[2]
        ]

    def autocomplete_suggest(self, cursor: int, search_split: []) -> str | None:
        # Suggest @
        if cursor == 0 and search_split[0] == '':
            return COMMAND_CHAR_SERVICE

        # In every other case, search should start with @
        if search_split[0] == COMMAND_CHAR_SERVICE:
            if cursor <= 1:
                if search_split[0] == COMMAND_CHAR_SERVICE:
                    commands = [
                        command for command in self.get_commands_registry().keys()
                        if command.startswith(''.join(search_split))
                    ]

                    return ' '.join(commands)

                elif search_split[0] == '':
                    return COMMAND_CHAR_SERVICE
            elif cursor == 2 or cursor == 3:
                if search_split[2] == COMMAND_SEPARATOR_ADDON:
                    search_service = ''.join(search_split[:3])
                    search = ''.join(search_split)

                    commands = [
                        command[len(search_service):] for command in self.get_commands_registry().keys()
                        if command.startswith(search)
                    ]

                    return ' '.join(commands)
                elif cursor == 2 and search_split[2] == ':':
                    # User types "core:", we add a second ":"
                    return ':'
            # Arguments
            elif cursor >= 4:
                return self.suggest_arguments(
                    ''.join(search_split[0:4]),
                    search_split[4:],
                )

        return None

    def locate_function(self, request) -> bool:
        """
            Support services inheritance, if a function is not found in a service,
            search it into parent service.
        """
        from src.helper.service import service_get_inheritance_tree
        request.match = self.build_match(request.command)

        if request.match:
            tree = service_get_inheritance_tree(
                self.kernel,
                to_snake_case(request.match[1]))

            for service_tree_item in tree:
                request.command = self.build_command_from_parts([
                    service_tree_item,
                    request.match[2],
                    request.match[3],
                ])

                if super().locate_function(request):
                    return True

        return False

    @classmethod
    def decorate_command(cls, function, kwargs):
        from addons.app.decorator.service_option import service_option
        return service_option(**kwargs)(function)