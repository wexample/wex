import datetime
import getpass
import os
import platform
import sys
from typing import TYPE_CHECKING, Any, Dict, List, Mapping, Optional, cast

import yaml

from addons.app.command.location.find import app__location__find
from addons.app.const.app import (
    APP_DIR_APP_DATA,
    APP_ENV_DEV,
    APP_ENV_LOCAL,
    APP_ENV_PROD,
    APP_ENV_TEST,
    APP_FILEPATH_REL_COMPOSE_RUNTIME_YML,
    APP_FILEPATH_REL_CONFIG,
    APP_FILEPATH_REL_CONFIG_RUNTIME,
    APP_FILEPATH_REL_DOCKER_ENV,
    APP_FILEPATH_REL_ENV,
    ERR_APP_NOT_FOUND,
    ERR_APP_SHOULD_RUN,
    PROXY_APP_NAME,
    PROXY_FILE_APPS_REGISTRY,
)
from src.const.globals import (
    COLOR_GRAY,
    COMMAND_TYPE_APP,
    COMMAND_TYPE_SERVICE,
    CORE_COMMAND_NAME,
    DATE_FORMAT_SECOND,
    SHELL_DEFAULT,
    VERBOSITY_LEVEL_MEDIUM,
)
from src.const.types import (
    AnyAppConfig,
    AnyCallable,
    AppConfig,
    AppConfigValue,
    AppDockerEnvConfig,
    AppRuntimeConfig,
    AppsPathsList,
    DockerCompose,
    StringKeysDict,
    StringsList,
    YamlContent,
)
from src.core.AddonManager import AddonManager
from src.core.FunctionProperty import FunctionProperty
from src.helper.args import args_push_one, args_shift_one
from src.helper.core import core_kernel_get_version
from src.helper.data_yaml import yaml_load, yaml_load_or_default, yaml_write
from src.helper.dict import dict_get_item_by_path
from src.helper.file import (
    file_env_to_dict,
    file_remove_dict_item_by_path,
    file_set_dict_item_by_path,
    file_write_dict_to_config,
)
from src.helper.service import service_load_config
from src.helper.string import string_to_kebab_case, string_to_snake_case

if TYPE_CHECKING:
    from src.core.CommandRequest import CommandRequest
    from src.core.Kernel import Kernel
    from src.core.response.AbstractResponse import AbstractResponse


class AppAddonManager(AddonManager):
    def __init__(
        self, kernel: "Kernel", name: str = COMMAND_TYPE_APP, app_dir: None | str = None
    ) -> None:
        super().__init__(kernel, name)
        self.app_dir: Optional[str] = None
        self.config: Optional[AppConfig] = None
        self.config_path: Optional[str] = None
        self.app_dirs_stack: List[str | None] = []
        self.runtime_config: Optional[AppRuntimeConfig] = None
        self.runtime_config_path: Optional[str] = None
        self.runtime_docker_compose: Optional[DockerCompose] = None
        self.runtime_docker_compose_path: Optional[str] = None
        self.first_log_indent: Optional[int] = None

        if app_dir:
            self.set_app_workdir(app_dir)

        # Register extra decorators to allow using it in yaml scripts
        from addons.app.decorator.app_command import app_command
        from addons.app.decorator.app_dir_option import app_dir_option
        from addons.app.decorator.app_webhook import app_webhook
        from addons.app.decorator.option_webhook_listener import option_webhook_listener
        from addons.app.decorator.service_option import service_option

        self.kernel.decorators["command"].update({"app_command": app_command})

        self.kernel.decorators["properties"].update(
            {
                "app_webhook": app_webhook,
                "app_dir_option": app_dir_option,
                "option_webhook_listener": option_webhook_listener,
                "service_option": service_option,
            }
        )

    def get_applications_path(self) -> str:
        return (
            os.sep
            + os.path.join("var", "www", self.kernel.registry_structure.content["env"])
            + os.sep
        )

    def get_env_file_path(self, file_relative_path: str, create: bool = False) -> str:
        relative_dir = os.path.dirname(file_relative_path)

        env_file_path = self.get_env_dir(relative_dir, create) + os.path.basename(
            file_relative_path
        )

        if create and not os.path.exists(env_file_path):
            with open(env_file_path, "w"):
                pass

        return env_file_path

    def get_env_dir(self, dir: str, create: bool = False) -> str:
        app_dir = self.get_app_dir_or_fail()

        env_dir = os.path.join(app_dir, APP_DIR_APP_DATA, dir) + os.sep

        if create and not os.path.exists(env_dir):
            os.makedirs(env_dir, exist_ok=True)

        return env_dir

    def load_script(self, name: str) -> Optional[YamlContent]:
        script_dir = self.get_env_file_path(os.path.join("script", name + ".yml"))

        return yaml_load(script_dir)

    def get_proxy_path(self) -> str:
        if platform.system() == "Darwin":
            return os.sep + os.path.join("Users", ".wex", "proxy") + os.sep
        else:
            return f"{self.get_applications_path()}{PROXY_APP_NAME}{os.sep}"

    def get_proxy_apps(self) -> AppsPathsList:
        return cast(
            AppsPathsList,
            yaml_load_or_default(self.get_proxy_path() + PROXY_FILE_APPS_REGISTRY, {}),
        )

    @classmethod
    def is_env_root(cls, app_dir: str) -> bool:
        if not os.path.exists(app_dir):
            return False

        # Search for config file.
        return os.path.exists(os.path.join(app_dir, APP_FILEPATH_REL_CONFIG))

    @classmethod
    def is_app_root(cls, app_dir: str) -> bool:
        if cls.is_env_root(app_dir):
            config = cls._load_config(os.path.join(app_dir, APP_FILEPATH_REL_CONFIG))

            return (
                "global" in config
                and "type" in config["global"]
                and config["global"]["type"] == "app"
            )
        return False

    @classmethod
    def _load_config(
        cls, path: str, default: Optional[YamlContent] = None
    ) -> YamlContent:
        return yaml_load(path, cast(YamlContent, default)) or {}

    def create_config(
        self, app_name: str, domains: Optional[StringsList] = None
    ) -> AppConfig:
        if domains is None:
            domains = []

        domain_main = (
            domains[0]
            if domains
            else f"{string_to_kebab_case(app_name)}.{CORE_COMMAND_NAME}"
        )
        email = f"contact@{domain_main}"

        return cast(
            AppConfig,
            {
                "global": {
                    "author": getpass.getuser(),
                    "created": datetime.datetime.utcnow().strftime(DATE_FORMAT_SECOND),
                    "name": app_name,
                    "services": [],
                    "type": "app",
                },
                "docker": {
                    "compose": {
                        "tty": True,
                        "stdin_open": True,
                    }
                },
                "env": {
                    APP_ENV_TEST: {
                        "domains": domains.copy(),
                        "domain_main": domain_main,
                        "email": email,
                    },
                    APP_ENV_LOCAL: {
                        "domains": domains.copy(),
                        "domain_main": domain_main,
                        "email": email,
                    },
                    APP_ENV_DEV: {
                        "domains": domains.copy(),
                        "domain_main": domain_main,
                        "email": email,
                    },
                    APP_ENV_PROD: {
                        "domains": domains.copy(),
                        "domain_main": domain_main,
                        "email": email,
                    },
                },
                "wex": {"version": core_kernel_get_version(self.kernel)},
            },
        )

    def _save_config(self, path: Optional[str], config: Optional[AnyAppConfig]) -> None:
        if not path or not config:
            return

        yaml_write(path, cast(YamlContent, config))

    def save_config(self) -> None:
        self._save_config(self.config_path, self.config)

    def save_runtime_config(self) -> None:
        self._save_config(self.runtime_config_path, self.runtime_config)

        app_dir: str = str(self.get_runtime_config("path.app"))

        app_env_path = os.path.join(app_dir, APP_FILEPATH_REL_ENV)

        env_dict: Dict[str, Any] = {"# .env config": True}

        env_dict.update(file_env_to_dict(app_env_path))

        config_path = os.path.join(app_dir, APP_FILEPATH_REL_DOCKER_ENV)

        env_dict.update({"# Build config": True})

        env_dict.update(self.config_to_docker_env())

        # Write as docker env file
        file_write_dict_to_config(env_dict, config_path)

    def config_to_docker_env(self) -> AppDockerEnvConfig:
        if not self.runtime_config or not self.config:
            return {}

        config = cast(StringKeysDict, self.config.copy())
        config["runtime"] = dict(sorted(self.runtime_config.items()))
        return self.dict_to_docker_env(config)

    def dict_to_docker_env(
        self, config: Mapping[str, Any], parent_key: str = "", sep: str = "_"
    ) -> AppDockerEnvConfig:
        items: List[Any] = []

        for k, v in config.items():
            new_key = parent_key + sep + k if parent_key else k
            new_key = string_to_snake_case(new_key)
            new_key = new_key.upper()
            if isinstance(v, Dict):
                items.extend(self.dict_to_docker_env(v, new_key, sep=sep).items())
            else:
                items.append((new_key, cast(Any, v)))

        return dict(items)

    def _set_config_value(
        self, config: Optional[AnyAppConfig], key: str, value: Any, replace: bool = True
    ) -> None:
        if not config:
            return None

        # Avoid "#refs" in files
        if isinstance(value, dict) or isinstance(value, list):
            value = value.copy()

        file_set_dict_item_by_path(self.config_to_dict(config), key, value, replace)

    def set_config(self, key: str, value: AppConfigValue, replace: bool = True) -> None:
        self._set_config_value(self.config, key, value, replace)

        self.save_config()

    def remove_config(self, key: str) -> None:
        file_remove_dict_item_by_path(self.config_to_dict(self.config), key)

        self.save_config()

    def remove_runtime_config(self, key: str) -> None:
        file_remove_dict_item_by_path(self.config_to_dict(self.config), key)

        self.save_runtime_config()

    def config_to_dict(self, config: Optional[AnyAppConfig]) -> StringKeysDict:
        if not config:
            return {}

        return cast(StringKeysDict, config)

    def set_runtime_config(
        self, key: str, value: AppConfigValue, replace: bool = True
    ) -> None:
        self._set_config_value(self.runtime_config, key, value, replace)

        self.save_runtime_config()

    def get_config(
        self, key: str, default: Optional[AppConfigValue] = None, required: bool = False
    ) -> AppConfigValue:
        return self._get_config_value(self.config, key, default, required)

    def _get_config_value(
        self,
        config: Optional[AppConfig | AppRuntimeConfig],
        key: str,
        default: Optional[AppConfigValue] = None,
        required: bool = False,
    ) -> AppConfigValue:
        if not config:
            return default

        value = dict_get_item_by_path(config, key, default)

        if required and value is None:
            self.kernel.io.error(
                f"Missing expected config key : {key}, got None", trace=False
            )

        return cast(AppConfigValue, value)

    def log(self, message: str, color: str = COLOR_GRAY, indent: int = 0) -> None:
        if self.first_log_indent is None:
            self.first_log_indent = self.kernel.io.log_indent

        if self.kernel.io.log_indent == self.first_log_indent:
            message = f'[{self.get_config("global.name")}] {message}'

        self.kernel.io.log(message, color, indent)

    def get_runtime_config(
        self, key: str, default: Optional[AppConfigValue] = None, required: bool = False
    ) -> AppConfigValue:
        return self._get_config_value(self.runtime_config, key, default, required)

    def ignore_app_dir(self, request: "CommandRequest") -> bool:
        if request.script_command is None:
            return False

        # Only specified commands will expect app location.
        # This is not a function property class.
        return (
            getattr(request.script_command.click_command, "app_command", False) == False
        )

    def hook_render_request_pre(self, request: "CommandRequest") -> None:
        if self.ignore_app_dir(request):
            return

        from src.core.command.ScriptCommand import ScriptCommand

        args = request.get_args_list()
        app_dir_arg = args_shift_one(args, "app-dir")
        request.first_arg = self
        script_command = cast(ScriptCommand, request.script_command)

        # User specified the app dir arg.
        if app_dir_arg is not None:
            app_dir_resolved = app_dir_arg
        else:
            # Previous app dir already exists.
            if self.app_dir is not None:
                app_dir_resolved = self.app_dir
            else:
                # Skip if the command allow to be executed without app location.
                if not FunctionProperty.get_property(
                    script_command, name="app_dir_required", default=False
                ):
                    self.app_dirs_stack.append(None)
                    self.unset_app_workdir()
                    return

                app_dir = os.getcwd() + os.sep

                app_dir_resolved = self.kernel.run_function(
                    app__location__find, {"app-dir": app_dir}
                ).first()

        if not app_dir_resolved:
            import logging

            self.kernel.io.error(
                ERR_APP_NOT_FOUND,
                {
                    "command": script_command,
                    "dir": app_dir_resolved,
                },
                logging.ERROR,
            )

            sys.exit(0)

        app_dir_resolved = str(app_dir_resolved)

        # Ensure it always ends with a /
        if not app_dir_resolved.endswith(os.sep):
            app_dir_resolved += os.sep

        # First test, create config.
        if self.app_dir != app_dir_resolved:
            self.set_app_workdir(app_dir_resolved)

        self.app_dirs_stack.append(app_dir_resolved)

        # Append to original apps list.
        request.args = args

        args_push_one(arg_list=args, arg_name="app-dir", value=app_dir_resolved)

        if (
            FunctionProperty.get_property(
                script_command=script_command, name="app_should_run", default=False
            )
            is True
        ):
            from addons.app.command.app.started import (
                APP_STARTED_CHECK_MODE_FULL,
                app__app__started,
            )

            if not self.kernel.run_function(
                app__app__started,
                {"app-dir": self.app_dir, "mode": APP_STARTED_CHECK_MODE_FULL},
            ).first():
                import logging

                self.kernel.io.error(
                    ERR_APP_SHOULD_RUN,
                    {
                        "command": request.string_command,
                        "dir": app_dir_resolved,
                    },
                    trace=False,
                )

    def get_app_dir_or_fail(self) -> str:
        if not self.app_dir:
            self.kernel.io.error("Trying to load app dir before initialization")
            assert False

        return self.app_dir

    def hook_render_request_post(self, response: "AbstractResponse") -> None:
        if not response.request or self.ignore_app_dir(response.request):
            return

        from src.helper.command import is_same_command

        # Ignore internally used command.
        if (
            not response.request
            or not response.request.script_command
            or is_same_command(response.request.script_command, app__location__find)
        ):
            return

        self.app_dirs_stack.pop()
        app_dir = (
            self.app_dirs_stack[-1]
            if len(self.app_dirs_stack)
            else self.kernel.get_path("call")
        )
        # Previous app dir was an app.
        if app_dir:
            # Reinit app dir if not the same.
            if app_dir != self.app_dir:
                self.set_app_workdir(app_dir)

    def add_proxy_app(self, name: str, app_dir: str) -> None:
        proxy_apps = self.get_proxy_apps()
        proxy_apps[name] = app_dir
        self.save_proxy_apps(proxy_apps)

    def save_proxy_apps(self, proxy_apps: AppsPathsList) -> None:
        with open(self.get_proxy_path() + PROXY_FILE_APPS_REGISTRY, "w") as f:
            yaml.dump(proxy_apps, f, indent=True)

    def set_app_workdir(self, app_dir: str) -> None:
        self.app_dir = app_dir
        self.config_path = os.path.join(app_dir, APP_FILEPATH_REL_CONFIG)
        self.runtime_config_path = os.path.join(
            app_dir, APP_FILEPATH_REL_CONFIG_RUNTIME
        )
        self.runtime_docker_compose_path = os.path.join(
            app_dir, APP_FILEPATH_REL_COMPOSE_RUNTIME_YML
        )
        self.load_config()

        if os.getcwd() != app_dir.rstrip(os.sep):
            self.kernel.io.log(
                "Switching to app : " + app_dir, verbosity=VERBOSITY_LEVEL_MEDIUM
            )

            os.chdir(app_dir)

    def load_config(self) -> None:
        if isinstance(self.config_path, str):
            self.config = cast(AppConfig, self._load_config(self.config_path))

        if isinstance(self.runtime_config_path, str):
            self.runtime_config = cast(
                AppRuntimeConfig, self._load_config(self.runtime_config_path)
            )

        if isinstance(self.runtime_docker_compose_path, str):
            self.runtime_docker_compose = cast(
                DockerCompose, self._load_config(self.runtime_docker_compose_path)
            )

    def unset_app_workdir(self, fallback_dir: str | None = None) -> None:
        self.app_dir = None
        self.config_path = None
        self.runtime_config_path = None
        self.runtime_docker_compose_path = None
        self.config = None
        self.runtime_config = None
        self.runtime_docker_compose = None

        if fallback_dir:
            # Print log in normal kernel.
            self.kernel.io.log(
                "Unset app dir to : " + fallback_dir, verbosity=VERBOSITY_LEVEL_MEDIUM
            )

            os.chdir(fallback_dir)

    def exec_in_app_workdir(self, app_dir: str, callback: AnyCallable) -> Any:
        app_dir_previous = os.getcwd() + os.sep
        self.set_app_workdir(app_dir)

        response = callback()

        self.set_app_workdir(app_dir_previous)

        return response

    def build_runtime_config(
        self, user: Optional[str] = None, group: Optional[str] = None
    ) -> None:
        import socket

        from addons.app.command.env.get import app__env__get
        from addons.app.command.hook.exec import app__hook__exec
        from src.const.globals import PASSWORD_INSECURE
        from src.helper.user import (
            get_gid_from_group_name,
            get_uid_from_user_name,
            get_user_group_name,
            get_user_or_sudo_user,
        )

        app_dir = self.get_app_dir_or_fail()
        env = self.kernel.run_function(app__env__get, {"app-dir": self.app_dir}).first()
        user = user or get_user_or_sudo_user()
        group = group or get_user_group_name(user)
        name = self.get_config("global.name")
        config = self.config

        if not config:
            return

        config = cast(AppConfig, config)

        self.log(f"Using user {user}:{group}")

        # Get a full config copy
        runtime_config = cast(AppRuntimeConfig, config.copy())
        # Add the per-environment config.
        runtime_config.update(config["env"][env])

        domains = []
        if "domains" in runtime_config:
            domains = runtime_config["domains"]

        if (
            "domain_main" in runtime_config
            and runtime_config["domain_main"] not in domains
        ):
            domains.append(runtime_config["domain_main"])

        # Add extra runtime config.
        runtime_config.update(
            {
                "domains": domains,
                "domains_string": ",".join(domains),
                "domain_tld": (
                    runtime_config["domain_tld"]
                    if "domain_tld" in runtime_config
                    else runtime_config["domain_main"]
                ),
                "env": env,
                "name": f"{name}_{env}",
                "host": {"ip": socket.gethostbyname(socket.gethostname())},
                "password": {"insecure": PASSWORD_INSECURE},
                "path": {
                    "app": app_dir,
                    "app_env": os.path.join(app_dir, APP_DIR_APP_DATA) + "/",
                    "proxy": self.get_proxy_path(),
                },
                "service": {},
                "started": False,
                "user": {
                    "group": group,
                    "gid": get_gid_from_group_name(group),
                    "name": user,
                    "uid": get_uid_from_user_name(user),
                },
            }
        )

        # Build paths to services docker compose yml files.
        for service, service_data in (
            self.kernel.resolvers[COMMAND_TYPE_SERVICE].get_registry_data().items()
        ):
            base_yml = service_data["dir"] + "docker/docker-compose.yml"
            env_yml = service_data["dir"] + f"docker/docker-compose.{env}.yml"

            if not os.path.exists(env_yml):
                env_yml = base_yml

            runtime_config["service"][service] = {
                "yml": {
                    "base": base_yml,
                    "env": env_yml,
                }
            }

        self.log(f"Build config file")

        self.runtime_config = runtime_config
        self.save_runtime_config()

        self.kernel.run_function(
            app__hook__exec, {"app-dir": self.app_dir, "hook": "config/runtime"}
        )

    def get_service_config(
        self, key: str, service: str | None = None, default: Optional[Any] = None
    ) -> Any:
        service = service or self.get_main_service()

        # Search into local config.
        return (
            self.get_config(f"service.{service}.{key}")
            # Search into the service config
            or dict_get_item_by_path(
                service_load_config(self.kernel, service), key, default
            )
        )

    def get_main_service(self) -> str:
        return str(self.get_config(key="global.main_service", required=True))

    def get_main_container_name(self) -> str:
        main_service = self.get_main_service()

        return (
            self.get_service_config(key="container.default", service=main_service)
            or main_service
        )

    def get_service_shell(self, service: str | None = None) -> Optional[str]:
        return (
            self.get_service_config(
                key="shell", service=(service or self.get_main_service())
            )
            or SHELL_DEFAULT
        )
