
def app_location_optional(function):
    # Say that the function is allowed to be executed without app location.
    function.app_location_optional = True
    return function
