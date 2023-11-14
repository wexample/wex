class FunctionProperty:
    property_name: str
    property_value: any = None

    def __init__(self, function, property_name: str, property_value: any = None):
        self.property_name = property_name or self.property_name
        self.property_value = property_value or self.property_value

        function.properties[property_name] = self

    @staticmethod
    def has_property(function, name: str) -> bool:
        return name in function.properties

    @staticmethod
    def get_property(function, name: str, default: any = None):
        return function.properties[name].property_value if name in function.properties else default
