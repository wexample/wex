from src.const.types import StringsList

APP_DIR_APP_DATA: str = '.wex/'
APP_DIR_TMP: str = f'{APP_DIR_APP_DATA}tmp/'
APP_ENV_DEV: str = 'dev'
APP_ENV_LOCAL: str = 'local'
APP_ENV_PROD: str = 'prod'
APP_ENV_TEST: str = 'test'
APP_ENVS: StringsList = [APP_ENV_LOCAL, APP_ENV_DEV, APP_ENV_PROD]
APP_NO_SSL_ENVS: StringsList = [APP_ENV_LOCAL, APP_ENV_TEST]
APP_FILE_APP_ENV: str = '.env'
APP_FILE_APP_CONFIG: str = 'config.yml'
APP_FILE_APP_SERVICE_CONFIG: str = 'service.config.yml'
APP_FILEPATH_REL_CONFIG: str = f'{APP_DIR_APP_DATA}{APP_FILE_APP_CONFIG}'
APP_FILEPATH_REL_CONFIG_RUNTIME: str = f'{APP_DIR_TMP}config.runtime.yml'
APP_FILEPATH_REL_COMPOSE_RUNTIME_YML: str = f'{APP_DIR_TMP}docker-compose.runtime.yml'
APP_FILEPATH_REL_DOCKER_ENV: str = f'{APP_DIR_TMP}docker.env'
APP_FILEPATH_REL_ENV: str = f'{APP_DIR_APP_DATA}{APP_FILE_APP_ENV}'
ERR_APP_NOT_FOUND: str = 'No application directory found when running "{command}", searching from {dir}'
ERR_APP_SHOULD_RUN: str = 'Application should be running to execute "{command}", in {dir}'
ERR_CORE_ACTION_NOT_FOUND: str = 'No core action found : "{command}"'
ERR_SERVICE_NOT_FOUND: str = 'Service not found : {service}'
PROXY_APP_NAME: str = 'wex-proxy'
PROXY_FILE_APPS_REGISTRY: str = 'apps.yml'
