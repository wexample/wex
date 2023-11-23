from typing import Optional

from src.core.file.YmlFileStructure import YmlFileStructure
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.Kernel import Kernel
    from const.types import KernelRegistry


class KernelRegistryFileStructure(YmlFileStructure):
    # May not exist when cache flushed
    should_exist: Optional[bool] = False
    kernel: 'Kernel'
    content: 'KernelRegistry'

    def __init__(self,
                 kernel: 'Kernel',
                 path: str,
                 initialize: bool = True) -> None:
        self.kernel = kernel

        super().__init__(
            path=path,
            initialize=initialize
        )

        # Always load at creation
        self.load_content(default={
            'env': None,
            'resolvers': {}
        })

    def build(self, test: bool = False, write: bool = True) -> 'KernelRegistry':
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

    def get_resolver_data(self, command_type: str):
        return self.content['resolvers'][command_type]
