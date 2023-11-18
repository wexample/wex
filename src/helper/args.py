import ast
import re
import click
from click.types import BoolParamType
from src.helper.string import to_kebab_case, to_snake_case
from typing import Any, Callable, Dict, Iterable, List, Union, Optional


def args_replace_one(
        arg_list: List[str],
        arg_name: str,
        value: Optional[Any] = None,
        is_flag: bool = False) -> Optional[str | bool]:
    previous = args_shift_one(
        arg_list=arg_list,
        arg_name=arg_name,
        is_flag=is_flag)

    args_push_one(
        arg_list=arg_list,
        arg_name=arg_name,
        value=value)

    return previous


def args_push_one(
        arg_list: List[str],
        arg_name: str,
        value: Optional[Any] = None) -> None:
    arg_list.append(f'--{arg_name}')

    if value is not None:
        arg_list.append(str(value))


def args_shift_one(
        arg_list: List[str],
        arg_name: str,
        is_flag: bool = False) -> Optional[str | bool]:
    """
    Alter arg list by removing arg names and returning arg value.
    Take arg name without dash, and remove args with any count of prefixed dashes.
    """
    arg_pattern = re.compile(r'(-+)' + re.escape(arg_name) + r'$')

    for i, arg in enumerate(arg_list):
        if isinstance(arg, str) and arg_pattern.match(arg):
            del arg_list[i]

            if is_flag:
                return True
            else:
                try:
                    next_value = arg_list.pop(i)
                    return next_value
                except IndexError:
                    return None
    return None


def args_split_arg_array(
        arg: Union[str, Iterable[str]],
        separator: str = ',') -> List[str]:
    if not arg:
        return []

    if isinstance(arg, str):
        arg = re.sub(r'[\[\]"\']', '', arg)
        return arg.split(separator)
    elif isinstance(arg, Iterable):
        return list(arg)


def args_convert_dict_to_long_names_dict(
        function: Callable,
        args: Dict[str, Any]) -> Dict[str, Any]:
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


def args_convert_dict_to_snake_dict(
        input_dict: Dict[str, Any]) -> Dict[str, Any]:
    return {to_snake_case(key): value for key, value in input_dict.items()}


def args_convert_dict_to_args(
        function: Callable,
        args: Dict[str, Any]) -> List[str]:
    """
    Convert args {"my-arg": "value"} to list ["--my_arg", "value"].
    Any key in `args` that is not found in `function.params` is added to the
    argument list as a key-value pair.
    """
    arg_list = []
    args_long = args_convert_dict_to_long_names_dict(function=function, args=args)
    args_long = args_convert_dict_to_snake_dict(input_dict=args_long)

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


def args_convert_to_dict(
        function: Callable,
        arg_list: List[str]) -> Dict[str, Any]:
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


def args_parse_one(
        argument: str,
        default: Optional[Any] = None) -> Any:
    if argument is None or argument == '':
        return default

    try:
        return ast.literal_eval(argument)
    except (ValueError, SyntaxError):
        return argument
