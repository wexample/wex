from src.const.globals import CORE_COMMAND_NAME
from src.helper.process import process_post_exec


def current_version_build(kernel):
    process_post_exec(kernel, [
        'dch',
        '--increment',
        '--package',
        CORE_COMMAND_NAME,
        'Update version'
    ])
