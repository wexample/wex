import datetime
import getpass
import os
import sys
from typing import TYPE_CHECKING, Any, Dict, List, Mapping, Optional, Union, cast

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
    ERR_APP_SHOULD_RUN,
    HELPER_APP_PROXY_SHORT_NAME,
    PROXY_FILE_APPS_REGISTRY,
)
from addons.app.helper.docker import DOCKER_COMPOSE_REL_PATH_BASE
from addons.app.src.AppCommand import AppCommand
from addons.app.src.file.AppDirectoryStructure import AppDirectoryStructure
from src.const.globals import (
    COLOR_GRAY,
    COMMAND_TYPE_APP,
    COMMAND_TYPE_SERVICE,
    CORE_COMMAND_NAME,
    DATE_FORMAT_SECOND,
    SHELL_DEFAULT,
    VERBOSITY_LEVEL_MEDIUM,
    VERSION_DEFAULT,
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
    StringKeysMapping,
    StringsList,
    YamlContent,
    YamlContentDict,
)
from src.core.AddonManager import AddonManager
from src.core.ConfigValue import ConfigValue
from src.helper.args import args_push_one, args_shift_one
from src.helper.core import core_kernel_get_version
from src.helper.data_yaml import yaml_load, yaml_load_dict, yaml_write
from src.helper.dict import dict_get_item_by_path, dict_has_item_by_path
from src.helper.file import (
    DICT_ITEM_EXISTS_ACTION_REPLACE,
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
        self._config: Optional[AppConfig] = None
        self._runtime_config: Optional[AppRuntimeConfig] = None

        self.app_dir: Optional[str] = None
        self.config_path: Optional[str] = None
        self.app_dirs_stack: List[str | None] = []
        self.runtime_config_path: Optional[str] = None
        self.runtime_docker_compose: Optional[DockerCompose] = None
        self.runtime_docker_compose_path: Optional[str] = None
        self.first_log_indent: Optional[int] = None
        self._directory: Optional[AppDirectoryStructure] = None

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

    def get_directory(self) -> AppDirectoryStructure:
        self._validate__should_not_be_none(self._directory)
        assert isinstance(self._directory, AppDirectoryStructure)

        return self._directory

    def get_app_name(self, default: Optional[str] = None) -> str:
        return self.get_config("global.name", default).get_str()

    def get_applications_path(self, environment: Optional[str] = None) -> str:
        return (
            os.sep
            + os.path.join(
                "var", "www", environment or self.kernel.registry_structure.content.env
            )
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
        app_dir = self.get_app_dir()

        env_dir = os.path.join(app_dir, APP_DIR_APP_DATA, dir) + os.sep

        if create and not os.path.exists(env_dir):
            os.makedirs(env_dir, exist_ok=True)

        return env_dir

    def load_script(self, name: str) -> Optional[YamlContent]:
        script_dir = self.get_env_file_path(os.path.join("script", name + ".yml"))

        return yaml_load(script_dir)

    def get_helper_app_name(self, short_name: str) -> str:
        return "-".join([CORE_COMMAND_NAME, short_name])

    def get_helper_app_path(
        self, short_name: str, environment: Optional[str] = None
    ) -> str:
        return f"{self.get_applications_path(environment)}{self.get_helper_app_name(short_name)}{os.sep}"

    def get_proxy_apps(self, environment: Optional[str] = None) -> AppsPathsList:
        return cast(
            AppsPathsList,
            yaml_load(
                self.get_helper_app_path(HELPER_APP_PROXY_SHORT_NAME, environment)
                + PROXY_FILE_APPS_REGISTRY,
                {},
            ),
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

    def is_valid_app(self) -> bool:
        return self.is_app_root(self.get_app_dir())

    @classmethod
    def _load_config(
        cls, path: str, default: Optional[YamlContentDict] = None
    ) -> YamlContentDict:
        return yaml_load_dict(path, default) or {}

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
                    "version": VERSION_DEFAULT,
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
        self._save_config(self.config_path, self._config)

    def save_runtime_config(self) -> None:
        self._save_config(self.runtime_config_path, self._runtime_config)

        app_dir: str = self.get_runtime_config("path.app").get_str()

        app_env_path = os.path.join(app_dir, APP_FILEPATH_REL_ENV)

        env_dict: Dict[str, Any] = {"# .env config": True}

        env_dict.update(file_env_to_dict(app_env_path))

        config_path = os.path.join(app_dir, APP_FILEPATH_REL_DOCKER_ENV)

        env_dict.update({"# Build config": True})

        env_dict.update(self.config_to_docker_env())

        # Write as docker env file
        file_write_dict_to_config(env_dict, config_path)

    def config_to_docker_env(self) -> AppDockerEnvConfig:
        if not self._runtime_config or not self._config:
            return {}

        config = cast(StringKeysDict, self._config.copy())
        config["runtime"] = dict(sorted(self._runtime_config.items()))
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
        self,
        config: Optional[AnyAppConfig],
        key: Union[str | StringsList],
        value: Any,
        when_exist: str = DICT_ITEM_EXISTS_ACTION_REPLACE,
    ) -> None:
        if not config:
            return None

        # Avoid "#refs" in files
        if isinstance(value, dict) or isinstance(value, list):
            value = value.copy()

        file_set_dict_item_by_path(self.config_to_dict(config), key, value, when_exist)

    def set_config(
        self,
        key: Union[str | StringsList],
        value: AppConfigValue,
        when_exist: str = DICT_ITEM_EXISTS_ACTION_REPLACE,
    ) -> None:
        self._set_config_value(self._config, key, value, when_exist)

        self.save_config()

    def remove_config(self, key: str) -> None:
        file_remove_dict_item_by_path(self.config_to_dict(self._config), key)

        self.save_config()

    def remove_runtime_config(self, key: str) -> None:
        file_remove_dict_item_by_path(self.config_to_dict(self._config), key)

        self.save_runtime_config()

    def config_to_dict(self, config: Optional[AnyAppConfig]) -> StringKeysDict:
        if not config:
            return {}

        return cast(StringKeysDict, config)

    def set_runtime_config(
        self,
        key: str,
        value: AppConfigValue,
        when_exist: str = DICT_ITEM_EXISTS_ACTION_REPLACE,
    ) -> None:
        self._set_config_value(self._runtime_config, key, value, when_exist)

        self.save_runtime_config()

    def get_runtime_config_content(self) -> AppRuntimeConfig:
        self._validate__should_not_be_none(self._runtime_config)
        assert isinstance(self._runtime_config, dict)

        return self._runtime_config

    def get_config_content(self) -> AppConfig:
        self._validate__should_not_be_none(self._config)
        assert isinstance(self._config, dict)

        return self._config

    def get_config(
        self, key: str, default: Optional[AppConfigValue] = None
    ) -> ConfigValue:
        return self._get_config_value(self.get_config_content(), key, default)

    def _get_config_value(
        self,
        config_dict: AppConfig | AppRuntimeConfig,
        key: str,
        default: Optional[AppConfigValue] = None,
    ) -> ConfigValue:
        value = dict_get_item_by_path(config_dict, key, default)

        if value is None and default is None:
            self.kernel.io.error(f'Trying to access undefined configuration "{key}"')

        return ConfigValue(value=value)

    def log(self, message: str, color: str = COLOR_GRAY, indent: int = 0) -> None:
        if self.app_dir:
            if self.first_log_indent is None:
                self.first_log_indent = self.kernel.io.log_indent

            if self.kernel.io.log_indent == self.first_log_indent:
                message = f"[{self.get_app_name()}] {message}"

        self.kernel.io.log(message, color, indent)

    def has_config(
        self, key: str, with_type: Optional[type] = None, accept_none: bool = False
    ) -> bool:
        if not self._config:
            return False

        config = self.get_config_content()
        value_exist = dict_has_item_by_path(config, key)

        if value_exist:
            value = dict_get_item_by_path(config, key)

            if with_type:
                return isinstance(value, with_type)

            if value is None:
                if accept_none:
                    return True
                else:
                    return False

        return value_exist

    def has_runtime_config(self, key: str) -> bool:
        return dict_has_item_by_path(cast(StringKeysMapping, self._runtime_config), key)

    def get_runtime_config(
        self, key: str, default: Optional[AppConfigValue] = None
    ) -> ConfigValue:
        return self._get_config_value(self.get_runtime_config_content(), key, default)

    def ignore_app_dir(self, request: "CommandRequest") -> bool:
        if request._script_command is None:
            return False

        # Only specified commands will expect app location.
        # This is not a function property class.
        return not isinstance(request.get_script_command(), AppCommand)

    def hook_render_request_pre(self, request: "CommandRequest") -> None:
        if self.ignore_app_dir(request):
            return

        args = request.get_args_list().copy()
        app_dir_arg = args_shift_one(args, "app-dir")
        request.first_arg = self
        script_command = request.get_script_command()

        # User specified the app dir arg.
        if app_dir_arg is not None:
            app_dir_resolved = app_dir_arg
        else:
            # Previous app dir already exists.
            if self.app_dir is not None:
                app_dir_resolved = self.app_dir
            else:
                # Skip if the command allow to be executed without app location.
                if not script_command.get_extra_value("app_dir_required", False):
                    self.app_dirs_stack.append(None)
                    self.unset_app_workdir()
                    return

                app_dir = os.getcwd() + os.sep

                app_dir_resolved = self.kernel.run_function(
                    app__location__find, {"app-dir": app_dir}
                ).first()

        if not app_dir_resolved:
            self.kernel.io.error(
                'No application directory found when running "{command}"',
                {
                    "command": request.get_string_command(),
                },
                trace=False,
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

        args_push_one(arg_list=args, arg_name="app-dir", value=app_dir_resolved)

        request.set_args_list(args)

        if script_command.get_extra_value("app_should_run", False):
            from addons.app.command.app.started import app__app__started

            if not self.kernel.run_function(
                app__app__started,
                {"app-dir": self.app_dir},
            ).first():
                from addons.app.command.app.start import app__app__start

                self.kernel.io.message_next_command(app__app__start)

                self.kernel.io.error(
                    ERR_APP_SHOULD_RUN,
                    {
                        "command": request.get_string_command(),
                        "dir": app_dir_resolved,
                    },
                    trace=False,
                )

        if script_command.get_extra_value("app_should_be_valid", False):
            structure = self.get_directory()
            structure.should_be_valid_app = True
            structure.initialize()

    def get_app_dir(self) -> str:
        self._validate__should_not_be_none(self.app_dir)
        assert isinstance(self.app_dir, str)

        return self.app_dir

    def hook_render_request_post(self, response: "AbstractResponse") -> None:
        request = response.get_request()

        if self.ignore_app_dir(
            request
        ) or not request.get_script_command().get_extra_value(
            "app_dir_required", False
        ):
            return

        from src.helper.command import is_same_command

        # Ignore internally used command.
        if is_same_command(request.get_script_command(), app__location__find):
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
        environment = self.get_env(app_dir)

        proxy_apps = self.get_proxy_apps(environment)
        proxy_apps[name] = app_dir

        self.save_proxy_apps(proxy_apps, environment)

    def save_proxy_apps(self, proxy_apps: AppsPathsList, environment: str) -> None:
        with open(
            self.get_helper_app_path(HELPER_APP_PROXY_SHORT_NAME, environment)
            + PROXY_FILE_APPS_REGISTRY,
            "w",
        ) as f:
            yaml.dump(proxy_apps, f, indent=True)

    def has_proxy_app(
        self, app_name: Optional[str] = None, environment: Optional[str] = None
    ) -> bool:
        environment = environment or self.get_env()

        if not app_name:
            if self.has_config("global.name"):
                app_name = self.get_app_name()
            else:
                return False

        proxy_apps = self.get_proxy_apps(environment)

        return app_name in proxy_apps

    def set_app_workdir(self, app_dir: str) -> None:
        self.app_dir = app_dir
        self.config_path = os.path.join(app_dir, APP_FILEPATH_REL_CONFIG)
        self.runtime_config_path = os.path.join(
            app_dir, APP_FILEPATH_REL_CONFIG_RUNTIME
        )
        self.runtime_docker_compose_path = os.path.join(
            app_dir, APP_FILEPATH_REL_COMPOSE_RUNTIME_YML
        )

        self._directory = AppDirectoryStructure(
            path=self.app_dir,
            # May be in invalid status at this point
            should_be_valid_app=False,
            # Do not apply changes
            initialize=False,
        )

        self.load_config()

        if os.getcwd() != app_dir.rstrip(os.sep):
            self.kernel.io.log(
                "Switching to app : " + app_dir, verbosity=VERBOSITY_LEVEL_MEDIUM
            )

            os.chdir(app_dir)

    def load_config(self) -> None:
        if isinstance(self.config_path, str):
            self._config = cast(AppConfig, self._load_config(self.config_path))

        if isinstance(self.runtime_config_path, str):
            self._runtime_config = cast(
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
        self._config = None
        self._runtime_config = None
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
        from src.helper.user import (
            get_gid_from_group_name,
            get_uid_from_user_name,
            get_user_group_name,
            get_user_or_sudo_user,
        )

        app_dir = self.get_app_dir()
        env = self.kernel.run_function(app__env__get, {"app-dir": self.app_dir}).first()
        user = user or get_user_or_sudo_user()
        group = group or get_user_group_name(user)
        name = self.get_app_name()
        config = self._config

        if not config:
            return

        config = cast(AppConfig, config)

        self.log(f"Using user {user}:{group}")

        # Get a full config copy
        runtime_config = cast(AppRuntimeConfig, config.copy())
        # Add the per-environment config.
        if env in config["env"]:
            runtime_config.update(config["env"][env])

        if any(k in runtime_config for k in ["domains", "domain_main", "domain_tld"]):
            domains = runtime_config.get("domains", [])

            if (
                runtime_config.get("domain_main")
                and runtime_config["domain_main"] not in domains
            ):
                domains.append(runtime_config["domain_main"])

            # Add extra runtime config.
            runtime_config.update(
                {
                    "domains": domains,
                    "domains_string": ",".join(domains),
                    "domain_tld": runtime_config.get(
                        "domain_tld", runtime_config.get("domain_main", "")
                    ),
                }
            )

        # Add extra runtime config.
        runtime_config.update(
            {
                "env": env,
                "name": f"{name}_{env}",
                "host": {"ip": socket.gethostbyname(socket.gethostname())},
                "path": {
                    "app": app_dir,
                    "app_env": os.path.join(app_dir, APP_DIR_APP_DATA) + "/",
                    "proxy": self.get_helper_app_path(HELPER_APP_PROXY_SHORT_NAME, env),
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
            base_yml = service_data["dir"] + DOCKER_COMPOSE_REL_PATH_BASE
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

        self._runtime_config = runtime_config
        self.save_runtime_config()

        self.kernel.run_function(
            app__hook__exec, {"app-dir": self.app_dir, "hook": "config/runtime"}
        )

    def has_service_config(
        self, key: str, service: str | None = None, default: Optional[Any] = None
    ) -> bool:
        service = service or (
            self.get_main_service() if self.has_main_service() else None
        )

        if not service:
            return False

        key = f"service.{service}.{key}"

        return self.has_config(key)

    def get_config_or_service_config(
        self, key: str, service: str | None = None, default: Optional[Any] = None
    ) -> ConfigValue:
        if self.has_config(key):
            return self.get_config(key)

        return self.get_service_config(key=key, service=service, default=default)

    def get_service_config(
        self, key: str, service: str | None = None, default: Optional[Any] = None
    ) -> ConfigValue:
        found_service = service or (
            self.get_main_service() if self.has_main_service() else None
        )

        service_config = (
            service_load_config(self.kernel, found_service) if found_service else None
        )

        return ConfigValue(
            dict_get_item_by_path(
                service_config,
                key,
                default,
            )
            if (found_service and service_config)
            else default
        )

    def has_main_service(self) -> bool:
        return self.has_config(key="global.main_service")

    def get_main_service(self) -> str:
        return self.get_config(key="global.main_service").get_str()

    def get_main_container_name(self) -> str:
        if not self.has_config(key="docker.main_container") and self.has_main_service():
            main_service = self.get_main_service()

            return self.get_service_config(
                key="container.default", service=main_service, default=main_service
            ).get_str()

        # If not exists, triggers error message on the best accurate configuration key.
        return self.get_config(key="docker.main_container").get_str()

    def get_service_shell(self, service: str | None = None) -> str:
        if not self.has_config(key="docker.main_container_shell"):
            if self.has_main_service():
                return self.get_service_config(
                    key="shell",
                    service=(service or self.get_main_service()),
                    default=SHELL_DEFAULT,
                ).get_str()

            return SHELL_DEFAULT

        return self.get_config(key="docker.main_container_shell").get_str()

    def get_services(self) -> StringKeysDict:
        return cast(StringKeysDict, self.get_config("service", {}).get_dict())

    def require_proxy(self) -> bool:
        return self.get_config_or_service_config(
            "require_proxy", default=False
        ).get_bool()

    def creates_network(self) -> bool:
        services = self.get_services()

        # Allow user to override any network expectation
        if self.has_config("docker.create_network"):
            return self.get_config("docker.create_network").get_bool()

        # App has at least one service who creates network.
        for service in services:
            if self.has_service_config("docker.create_network"):
                if self.get_service_config(
                    key="docker.create_network", service=service, default=False
                ).get_bool():
                    self.kernel.io.log(f"{service} needs a docker network")
                    return True

        # App does not requires proxy.
        if not self.require_proxy():
            return True

        return False

    def get_env_var(self, key: str) -> Optional[str]:
        from dotenv import dotenv_values

        app_env_path = os.path.join(self.get_app_dir(), APP_FILEPATH_REL_ENV)
        value = dotenv_values(app_env_path).get(key)

        return str(value) if value else None

    def get_env(self, app_dir: Optional[str] = None) -> str:
        from addons.app.command.env.get import _app__env__get

        env = _app__env__get(self.kernel, app_dir or self.get_app_dir())
        assert isinstance(env, str)

        return env

    def app_is_reverse_proxy(self, app_dir: Optional[str] = None) -> bool:
        from addons.app.command.service.used import app__service__used

        return bool(
            self.kernel.run_function(
                app__service__used,
                {"service": "proxy", "app-dir": app_dir or self.get_app_dir()},
            ).first()
        )
