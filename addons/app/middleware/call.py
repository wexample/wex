import os

from addons.app.command.location.find import app__location__find


def app_middleware_call(kernel, command, args) -> None:
    app_dir = os.getcwd()

    kernel.addons['app']['path']['call_app_dir'] = app__location__find.callback(
        app_dir
    )
