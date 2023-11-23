from typing import Callable


class ScriptCommand:
    function: Callable

    def __init__(self, function):
        self.function = function
