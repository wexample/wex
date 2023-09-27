
def app_dir_optional(function):
    # Say that the function is allowed to be executed without app location.
    function.app_dir_optional = True
    return function
