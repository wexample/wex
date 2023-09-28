import ast
import re
import click
from typing import Iterable, Union, List
from click.types import BoolParamType

from src.helper.string import to_kebab_case, to_snake_case


def split_arg_array(arg: Union[str, Iterable], separator: str = ',') -> List[str]:
    if not arg:
        return []

    if isinstance(arg, str):
        arg = re.sub(r'[\[\]"\']', '', arg)
        return arg.split(separator)
    elif isinstance(arg, Iterable):
        return list(arg)


def convert_args_to_long_names_dict(function, args: dict):
    return convert_dict_to_long_names_dict(
        function,
        convert_args_to_dict(
            function,
            args
        )
    )


def convert_dict_to_long_names_dict(function, args: dict):
    short_names = {}
    for param in function.params:
        for opt in param.opts:
            # This is a short name
            if opt.startswith('-') and opt[1:2] != '-':
                short_names[opt[1:]] = to_kebab_case(param.name)

    # Transform short named args to long named args.
    args_long = {}
    for name in args:
        if name in short_names:
            args_long[short_names[name]] = args[name]
        else:
            args_long[name] = args[name]

    return args_long


def convert_dict_to_snake_dict(dict: dict):
    return {to_snake_case(key): value for key, value in dict.items()}


def convert_dict_to_args(function, args: dict):
    """
    Convert args {"my-arg": "value"} to list ["--my_arg", "value"].
    Any key in `args` that is not found in `function.params` is added to the
    argument list as a key-value pair.
    """
    arg_list = []
    args_long = convert_dict_to_long_names_dict(function, args)
    args_long = convert_dict_to_snake_dict(args_long)

    for param in function.params:
        if param.name in args_long:
            if isinstance(param, click.Option):
                param_name_kebab = to_kebab_case(param.name)

                if param.is_flag:
                    if args_long[param.name]:
                        arg_list.append(f'--{param_name_kebab}')
                    # Flag passed to False is just removed
                elif args_long[param.name] is not None:
                    arg_list.append(f'--{param_name_kebab}')
                    value = args_long[param.name]
                    if not isinstance(args_long[param.name], bool):
                        value = str(value)
                    arg_list.append(value)
    # Append any remaining arguments as key-value pairs
    for key, value in args_long.items():
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


def parse_arg(argument, default=None):
    if argument is None or argument == '':
        return default

    try:
        return ast.literal_eval(argument)
    except (ValueError, SyntaxError):
        return argument
