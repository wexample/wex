from src.core.command.resolver.AddonCommandResolver import AddonCommandResolver
from src.core.command.resolver.AppCommandResolver import AppCommandResolver
from src.core.command.resolver.ServiceCommandResolver import ServiceCommandResolver
from src.core.command.resolver.UserCommandResolver import UserCommandResolver

COMMAND_RESOLVERS_CLASSES = [
    AddonCommandResolver,
    ServiceCommandResolver,
    AppCommandResolver,
    UserCommandResolver,
]