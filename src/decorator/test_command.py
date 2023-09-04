def test_command(function):
    # Say that the function is not allowed to be executed without sudo permissions.
    function.test_command = True
    return function
