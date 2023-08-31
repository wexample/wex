def app_middleware_init(kernel, **kwargs) -> None:
    kernel.addons['app'].set_app_workdir()
