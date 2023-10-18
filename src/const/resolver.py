from src.core.command.AddonCommandResolver import AddonCommandResolver
from src.core.command.AppCommandResolver import AppCommandResolver
from src.core.command.ServiceCommandResolver import ServiceCommandResolver
from src.core.command.UserCommandResolver import UserCommandResolver

COMMAND_RESOLVERS_CLASSES = [
    AddonCommandResolver,
    ServiceCommandResolver,
    AppCommandResolver,
    UserCommandResolver,
]