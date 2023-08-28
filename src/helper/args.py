import ast
import re
import click
from typing import Iterable, Union, List
from click.types import BoolParamType


def split_arg_array(arg: Union[str, Iterable], separator: str = ',') -> List[str]:
    if not arg:
        return []

    if isinstance(arg, str):
        arg = re.sub(r'[\[\]"\']', '', arg)
        return arg.split(separator)
    elif isinstance(arg, Iterable):
        return list(arg)


def convert_dict_to_args(function, args):
    """
    Convert args {"arg": "value"} to list ["--arg", "value"].
    Any key in `args` that is not found in `function.params` is added to the
    argument list as a key-value pair.
    """
    arg_list = []
    for param in function.params:
        if param.name in args:
            if isinstance(param, click.Option):
                if param.is_flag:
                    if args[param.name]:
                        arg_list.append(f'--{param.name}')
                    # Flag passed to False is just removed
                elif args[param.name] is not None:
                    arg_list.append(f'--{param.name}')
                    if not isinstance(args[param.name], bool):
                        # Convert to str to allow joining array.
                        arg_list.append(str(args[param.name]))
    # Append any remaining arguments as key-value pairs
    for key, value in args.items():
        if key not in [param.name for param in function.params] and value is not None:
            arg_list.append(f'--{key}')
            if not isinstance(value, bool):
                # Convert to str to allow joining array.
                arg_list.append(str(value))
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


def parse_arg(argument):
    if argument == None or argument == '':
        return argument

    try:
        return ast.literal_eval(argument)
    except (SyntaxError, ValueError) as argument:
        return argument
