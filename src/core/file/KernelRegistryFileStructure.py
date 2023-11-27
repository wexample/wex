from typing import TYPE_CHECKING, Optional, cast

from src.const.types import KernelRegistry, RegistryResolverData
from src.core.file.YmlFileStructure import YmlFileStructure

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


class KernelRegistryFileStructure(YmlFileStructure):
    # May not exist when cache flushed
    should_exist: Optional[bool] = False
    kernel: 'Kernel'
    content: KernelRegistry

    def __init__(self,
                 kernel: 'Kernel',
                 path: str,
                 initialize: bool = True) -> None:
        self.kernel = kernel

        super().__init__(
            path=path,
            initialize=initialize
        )

        default: KernelRegistry = KernelRegistry(env=None, resolvers={})

        # Always load at creation
        self.load_content(default=default)

    def build(self, test: bool = False, write: bool = True) -> KernelRegistry:
        from addons.app.command.env.get import _app__env__get

        self.kernel.io.log('Building registry...')

        # Call function avoiding core command management.
        self.content['env'] = _app__env__get(
            self.kernel.directory.path
        )

        for command_type in self.kernel.resolvers:
            self.content['resolvers'][command_type] = self.kernel.resolvers[command_type].build_registry_data(test)

        if write:
            self.write_content()

        return self.content

    def get_resolver_data(self, command_type: str) -> RegistryResolverData:
        return cast(RegistryResolverData, self.content['resolvers'][command_type])
