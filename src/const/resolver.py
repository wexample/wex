from src.core.command_resolver.AddonCommandResolver import AddonCommandResolver
from src.core.command_resolver.AppCommandResolver import AppCommandResolver
from src.core.command_resolver.ServiceCommandResolver import ServiceCommandResolver
from src.core.command_resolver.UserCommandResolver import UserCommandResolver

COMMAND_RESOLVERS_CLASSES = [
    AddonCommandResolver,
    ServiceCommandResolver,
    AppCommandResolver,
    UserCommandResolver,
]