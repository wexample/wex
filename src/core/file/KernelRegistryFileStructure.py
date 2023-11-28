from typing import TYPE_CHECKING, Optional, cast

from src.const.types import (
    BasicValue,
    KernelRegistry,
    RegistryResolverData,
    YamlContent,
)
from src.core.file.YmlFileStructure import YmlFileStructure

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


class KernelRegistryFileStructure(YmlFileStructure):
    # May not exist when cache flushed
    should_exist: Optional[bool] = False
    kernel: "Kernel"
    content: KernelRegistry

    def __init__(self, kernel: "Kernel", path: str, initialize: bool = True) -> None:
        self.kernel = kernel

        super().__init__(path=path, initialize=initialize)

        # Always load at creation
        self.load_content()

    def load_content(self, default: Optional[YamlContent] = None) -> None:
        content = self.load_content_yaml(default)

        self.content = KernelRegistry(
            env=content["env"] if content else None,
            resolvers=content["resolvers"] if content else {},
        )

    def build(self, test: bool = False, write: bool = True) -> KernelRegistry:
        from addons.app.command.env.get import _app__env__get

        self.kernel.io.log("Building registry...")

        # Call function avoiding core command management.
        self.content.env = _app__env__get(self.kernel, self.kernel.directory.path)
        self.content.resolvers = {}

        for command_type in self.kernel.resolvers:
            self.content.resolvers[command_type] = self.kernel.resolvers[
                command_type
            ].build_registry_data(test)

        if write:
            self.write_content()

        return self.content

    def get_resolver_data(self, command_type: str) -> RegistryResolverData:
        return self.content.resolvers[command_type]

    def get_writable_content(self) -> BasicValue:
        return self.content.to_dict()
