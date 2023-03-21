import click
from click.types import BoolParamType


def convert_dict_to_args(obj):
    """
    Convert a dictionary to a list of arguments.
    {'arg': 'value'} becomes ['--arg', 'value'].
    If the value is a bool, it becomes just ['--arg'] for True, and it is omitted for False.
    """
    arg_list = []
    for key, value in obj.items():
        arg_list.append(f'--{key}')

        if not isinstance(value, bool):
            arg_list.append(value)

    return arg_list


def convert_args_to_dict(function, arg_list):
    args_dict = {}
    param_dict = {
        opt.lstrip('-'): param
        for param in function.params if isinstance(param, click.Option)
        for opt in param.opts
    }

    i = 0
    while i < len(arg_list):
        arg = arg_list[i]

        if isinstance(arg, str):
            stripped_arg = arg.lstrip('-')

            # Manage parameters defined in function
            if stripped_arg in param_dict:
                param = param_dict[stripped_arg]
                if isinstance(param.type, BoolParamType) or param.is_flag:
                    args_dict[stripped_arg] = True
                    i += 1
                else:
                    i += 1
                    value = arg_list[i]
                    args_dict[stripped_arg] = value
                    i += 1
            # Manage unknown parameters
            else:
                key = arg.lstrip('-')

                if len(arg_list) > i + 1 and arg_list[i + 1][0:1] != '-':
                    args_dict[key] = arg_list[i + 1]
                    i += 1
                else:
                    args_dict[key] = True

                i += 1
        else:
            i += 1

    return args_dict
