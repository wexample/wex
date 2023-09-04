
def as_sudo(function):
    # Say that the function is not allowed to be executed without sudo permissions.
    function.as_sudo = True
    return function
