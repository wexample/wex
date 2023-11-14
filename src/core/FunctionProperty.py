class FunctionProperty:
    property_name: str
    property_value: any

    def __init__(self, function, property_name: str = None, property_value: any = None):
        self.property_name = property_name or self.property_name
        self.property_value = property_value or self.property_value

        function.properties[property_name] = self

    def get_property_value(self):
        return self.property_value

    @staticmethod
    def has_property(function, name: str):
        return name in function.properties
