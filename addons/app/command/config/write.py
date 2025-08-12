import os
import pwd
import grp
import subprocess
from typing import TYPE_CHECKING, Optional

import yaml

from addons.app.command.hook.exec import app__hook__exec
from addons.app.const.app import APP_FILEPATH_REL_COMPOSE_RUNTIME_YML
from addons.app.decorator.app_command import app_command
from addons.app.helper.docker import (
    docker_exec_app_compose,
    docker_get_app_compose_files,
)
from src.decorator.option import option
from src.helper.prompt import prompt_progress_steps

if TYPE_CHECKING:
    from addons.app.AppAddonManager import AppAddonManager


@app_command(
    help="Write the configuration file for services to start", should_be_valid=True
)
@option("--user", "-u", type=str, required=False, help="Owner of application files")
@option("--group", "-g", type=str, required=False, help="Group of application files")
def app__config__write(
    manager: "AppAddonManager",
    app_dir: str,
    user: Optional[str] = None,
    group: Optional[str] = None,
) -> None:
    kernel = manager.kernel

    def _app__config__write__runtime() -> None:
        nonlocal user
        nonlocal group

        manager.build_runtime_config(user, group)

    def _app__config__write__docker() -> None:
        kernel.run_function(
            app__hook__exec, {"app-dir": app_dir, "hook": "config/write-compose-pre"}
        )

        compose_files = docker_get_app_compose_files(manager, app_dir)

        if not len(compose_files) != 0:
            manager.log("No docker compose file")
            return

        # Debug permissions juste avant l'appel à docker compose
        try:
            def _fmt_stat(p: str) -> str:
                st = os.stat(p)
                user = pwd.getpwuid(st.st_uid).pw_name
                group = grp.getgrgid(st.st_gid).gr_name
                mode = oct(st.st_mode & 0o777)
                return f"path={p} owner={user}:{group} mode={mode}"

            paths = [
                "/var",
                "/var/www",
                "/var/www/test",
                "/var/www/test/wex-proxy",
                "/var/www/test/wex-proxy/.wex",
                "/var/www/test/wex-proxy/.wex/tmp",
                "/var/www/test/wex-proxy/.wex/tmp/docker.env",
                os.path.join(app_dir, ".wex"),
                os.path.join(app_dir, ".wex", "tmp"),
                os.path.join(app_dir, ".wex", "tmp", "docker.env"),
            ]
            print(f"[compose-debug] EUID={os.geteuid()} EGID={os.getegid()}")
            for p in paths:
                if os.path.exists(p):
                    try:
                        print("[compose-debug]", _fmt_stat(p))
                        out = subprocess.run(["/bin/ls", "-lLd", p], capture_output=True, text=True)
                        print("[compose-debug]", out.stdout.strip())
                    except Exception as e:
                        print(f"[compose-debug] stat/ls failed for {p}: {e}")
                else:
                    print(f"[compose-debug] missing: {p}")

            # Vérifier explicitement l'accès en tant que 'owner'
            env_file = "/var/www/test/wex-proxy/.wex/tmp/docker.env"
            if os.path.exists(env_file):
                for cmd in (
                    ["sudo", "-n", "-u", "owner", "stat", env_file],
                    ["sudo", "-n", "-u", "owner", "head", "-n1", env_file],
                ):
                    try:
                        res = subprocess.run(cmd, capture_output=True, text=True)
                        print(f"[compose-debug] run {' '.join(cmd)} -> rc={res.returncode}")
                        if res.stdout:
                            print("[compose-debug] stdout:", res.stdout.strip())
                        if res.stderr:
                            print("[compose-debug] stderr:", res.stderr.strip())
                    except Exception as e:
                        print(f"[compose-debug] failed to run {' '.join(cmd)}: {e}")
        except Exception as e:
            print(f"[compose-debug] permission debug failed: {e}")

        manager.log(f"Compiling docker compose file...")
        yml_content = str(
            docker_exec_app_compose(kernel, app_dir, compose_files, "config")
        )

        try:
            yaml.safe_load(yml_content)
        except yaml.YAMLError:
            kernel.io.print(yml_content)

            kernel.io.error("Wrong yaml from docker compose")

        with open(
            os.path.join(app_dir, APP_FILEPATH_REL_COMPOSE_RUNTIME_YML), "w"
        ) as f:
            f.write(yml_content)

        kernel.run_function(
            app__hook__exec, {"app-dir": app_dir, "hook": "config/write-post"}
        )

    prompt_progress_steps(
        kernel,
        [
            _app__config__write__runtime,
            _app__config__write__docker,
        ],
    )
