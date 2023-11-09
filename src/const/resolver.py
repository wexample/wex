from src.core.command_runner.AddonCommandResolver import AddonCommandResolver
from src.core.command_runner.AppCommandResolver import AppCommandResolver
from src.core.command_runner.ServiceCommandResolver import ServiceCommandResolver
from src.core.command_runner.UserCommandResolver import UserCommandResolver

COMMAND_RESOLVERS_CLASSES = [
    AddonCommandResolver,
    ServiceCommandResolver,
    AppCommandResolver,
    UserCommandResolver,
]