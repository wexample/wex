
def no_log(function):
    # Say that the function is not allowed to be executed without sudo permissions.
    function.no_log = True
    return function
