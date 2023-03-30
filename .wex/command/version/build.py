from src.helper.process import process_post_exec


def current_version_build(kernel):
    process_post_exec(kernel, [
        'dch',
        '--increment',
        '--package',
        'wex',
        'Update version'
    ])
