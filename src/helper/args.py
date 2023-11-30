import ast
import re
from typing import Any, Dict, Iterable, List, Optional, Union, cast

import click
from click.core import Command
from click.types import BoolParamType

from src.const.types import (
    BasicValue,
    CoreCommandArgsDict,
    CoreCommandArgsList,
    StringKeysDict,
    StringsList,
)
from src.helper.string import string_to_kebab_case, string_to_snake_case


def args_replace_one(
    arg_list: List[str],
    arg_name: str,
    value: Optional[Any] = None,
    is_flag: bool = False,
) -> Optional[str | bool]:
    previous = args_shift_one(arg_list=arg_list, arg_name=arg_name, is_flag=is_flag)

    args_push_one(arg_list=arg_list, arg_name=arg_name, value=value)

    return previous


def args_push_one(
    arg_list: List[str], arg_name: str, value: Optional[Any] = None
) -> None:
    arg_list.append(f"--{arg_name}")

    if value is not None:
        arg_list.append(str(value))


def args_shift_one(
    arg_list: List[str], arg_name: str, is_flag: bool = False
) -> Optional[str | bool]:
    """
    Alter arg list by removing arg names and returning arg value.
    Take arg name without dash, and remove args with any count of prefixed dashes.
    """
    arg_pattern = re.compile(r"(-+)" + re.escape(arg_name) + r"$")

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
    arg: Union[str, Iterable[str]], separator: str = ","
) -> StringsList:
    if not arg:
        return []

    if isinstance(arg, str):
        arg = re.sub(r'[\[\]"\']', "", arg)
        return [item.strip() for item in arg.split(separator)]
    elif isinstance(arg, Iterable):
        return [item.strip() for item in arg]


def args_convert_dict_to_long_names_dict(
    function: Command, args: Dict[str, Any]
) -> Dict[str, Any]:
    short_names = {}
    for param in function.params:
        for opt in param.opts:
            # This is a short name
            if opt.startswith("-") and opt[1:2] != "-":
                if param.name:
                    short_names[opt[1:]] = string_to_kebab_case(param.name)

    # Transform short named args to long named args.
    args_long = {}
    for name in args:
        if name in short_names:
            args_long[short_names[name]] = args[name]
        else:
            args_long[name] = args[name]

    return args_long


def args_convert_dict_to_snake_dict(input_dict: Dict[str, Any]) -> Dict[str, Any]:
    return {string_to_snake_case(key): value for key, value in input_dict.items()}


def args_convert_dict_to_args(
    function: Command, args: CoreCommandArgsDict
) -> CoreCommandArgsList:
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
                param_name_kebab = string_to_kebab_case(param.name)

                if param.is_flag:
                    if args_long[param.name]:
                        arg_list.append(f"--{param_name_kebab}")
                    # Flag passed to False is just removed
                elif args_long[param.name] is not None:
                    arg_list.append(f"--{param_name_kebab}")
                    value = args_long[param.name]
                    if not isinstance(args_long[param.name], bool):
                        value = str(value)
                    arg_list.append(value)
    # Append any remaining arguments as key-value pairs
    for key, value in args_long.items():
        if key not in [param.name for param in function.params] and value is not None:
            arg_list.append(f"--{key}")
            if not isinstance(value, bool):
                # Convert to str to allow joining array.
                arg_list.append(str(value))

    return arg_list


def args_convert_to_dict(function: Command, arg_list: List[str]) -> Dict[str, Any]:
    args_dict: Dict[str, str | bool] = {}

    param_dict = {
        opt.lstrip("-"): param
        for param in function.params
        if isinstance(param, click.Option)
        for opt in param.opts
    }

    i = 0
    while i < len(arg_list):
        arg = arg_list[i]

        if isinstance(arg, str):
            stripped_arg = arg.lstrip("-")

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
                key = arg.lstrip("-")

                if len(arg_list) > i + 1 and arg_list[i + 1][0:1] != "-":
                    args_dict[key] = arg_list[i + 1]
                    i += 1
                else:
                    args_dict[key] = True

                i += 1
        else:
            i += 1

    return args_dict


def args_parse_dict(arg: str) -> StringKeysDict:
    arg_dict = args_parse_one(arg, {})

    if not isinstance(arg_dict, dict):
        return {}

    return arg_dict


def args_parse_one(argument: str, default: Optional[Any] = None) -> BasicValue:
    if argument is None or argument == "":
        return default

    try:
        parsed = ast.literal_eval(argument)
        if arg_is_basic_value(parsed):
            return cast(BasicValue, parsed)
        return default
    except (ValueError, SyntaxError):
        return argument


def arg_is_basic_value(value: Any) -> bool:
    """
    Check if the value is compatible with basic YAML types
    """

    yaml_basic_types = (str, int, float, bool, type(None))

    if isinstance(value, yaml_basic_types):
        return True

    elif isinstance(value, list):
        return all(arg_is_basic_value(item) for item in value)

    elif isinstance(value, dict):
        return all(
            isinstance(key, str) and arg_is_basic_value(val)
            for key, val in value.items()
        )

    else:
        return False
