APP_DIR_APP_DATA = '.wex/'
APP_DIR_TMP = f'{APP_DIR_APP_DATA}tmp/'
APP_ENV_DEV = 'dev'
APP_ENV_LOCAL = 'local'
APP_ENV_PROD = 'prod'
APP_ENVS = [APP_ENV_LOCAL, APP_ENV_DEV, APP_ENV_PROD]
APP_FILE_APP_ENV = '.env'
APP_FILE_APP_CONFIG = 'config.yml'
APP_FILE_APP_SERVICE_CONFIG = 'service.config.yml'
APP_FILEPATH_REL_CONFIG = f'{APP_DIR_APP_DATA}{APP_FILE_APP_CONFIG}'
APP_FILEPATH_REL_CONFIG_RUNTIME = f'{APP_DIR_TMP}config.runtime.yml'
APP_FILEPATH_REL_COMPOSE_RUNTIME_YML = f'{APP_DIR_TMP}docker-compose.runtime.yml'
APP_FILEPATH_REL_DOCKER_ENV = f'{APP_DIR_TMP}docker.env'
APP_FILEPATH_REL_ENV = f'{APP_DIR_APP_DATA}{APP_FILE_APP_ENV}'
ERR_APP_NOT_FOUND = 'ERR_APP_NOT_FOUND'
ERR_CORE_ACTION_NOT_FOUND = 'ERR_CORE_ACTION_NOT_FOUND'
ERR_SERVICE_NOT_FOUND = 'ERR_SERVICE_NOT_FOUND'
PROXY_APP_NAME = 'wex-proxy'
PROXY_FILE_APPS_REGISTRY = 'apps.yml'
