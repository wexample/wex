from src.const.globals import CORE_COMMAND_FILE
from src.helper.args import convert_dict_to_args
from src.helper.command import build_command_from_function


def process_post_exec(kernel, args):
    # Print joined command in a post process file.
    with open(kernel.path['tmp'] + '/process/' + str(kernel.process_id) + '.post-exec', 'a') as f:
        f.write(
            ' '.join(['"' + arg + '"' if ' ' in arg else arg for arg in args])
            + '\n'
        )


def process_post_exec_wex(kernel, function: callable, args={}, is_async=False):
    command = [
        'bash',
        CORE_COMMAND_FILE,
        build_command_from_function(function),
    ] + convert_dict_to_args(function, args)

    if is_async:
        command.insert(0, 'nohup')
        command += ['>', '/dev/null', '2>&1', '&']

    process_post_exec(
        kernel,
        command
    )
