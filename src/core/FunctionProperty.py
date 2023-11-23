from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.command.ScriptCommand import ScriptCommand


class FunctionProperty:
    property_name: str
    property_value: any = None

    def __init__(self, script_command: 'ScriptCommand', property_name: str, property_value: any = None) -> None:
        self.property_name = property_name or self.property_name
        self.property_value = property_value or self.property_value

        script_command.function.properties[property_name] = self

    @staticmethod
    def has_property(script_command: 'ScriptCommand', name: str) -> bool:
        return name in script_command.function.properties

    @staticmethod
    def get_property(script_command: 'ScriptCommand', name: str, default: any = None):
        return script_command.function.properties[
            name].property_value if name in script_command.function.properties else default
