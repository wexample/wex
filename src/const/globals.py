COLOR_BLUE = "\033[0;34m"
COLOR_CYAN = "\033[0;36m"
COLOR_DEFAULT = "\033[0m"
COLOR_GRAY = '\033[0;90m'
COLOR_GREEN = "\033[0;32m"
COLOR_LIGHT_BLUE = "\033[0;34m"
COLOR_LIGHT_CYAN = "\033[0;36m"
COLOR_LIGHT_GRAY = "\033[0;37m"
COLOR_LIGHT_GREEN = "\033[0;32m"
COLOR_LIGHT_MAGENTA = "\033[0;35m"
COLOR_LIGHT_RED = "\033[0;31m"
COLOR_LIGHT_YELLOW = "\033[0;93m"
COLOR_MAGENTA = "\033[0;35m"
COLOR_RED = "\033[0;31m"
COLOR_RESET = '\033[0m'
COLOR_WHITE = "\033[0;37m"
COLOR_YELLOW = "\033[0;33m"
COLOR_BLACK = "\033[0;30m"
COMMAND_SEPARATOR_ADDON = '::'
COMMAND_SEPARATOR_FUNCTION_PARTS = '__'
COMMAND_SEPARATOR_GROUP = '/'
COMMAND_TYPE_ADDON = 'addon'
COMMAND_TYPE_APP = 'app'
COMMAND_TYPE_SERVICE = 'service'
COMMAND_TYPE_USER = 'user'
COMMAND_TYPE_CORE = 'core'
COMMAND_CHAR_APP = '.'
COMMAND_CHAR_SERVICE = '@'
COMMAND_CHAR_USER = '~'
COMMAND_PATTERN_ADDON = r'^(?:([\w_-]+)::)?([\w_-]+)/([\w_-]+)$'
COMMAND_PATTERN_APP = r'^(\.)([\w_-]+)/([\w_-]+)$'
COMMAND_PATTERN_SERVICE = r'^@([\w_-]+)::([\w_-]+)/([\w_-]+)$'
COMMAND_PATTERN_USER = r'(^~)([\w_-]+)/([\w_-]+)$'
COMMAND_PATTERN_CORE = r'^()()([a-z-_]+)$'
CONFIG_SEPARATOR_DEFAULT = '='
CORE_BIN_FILE_ROOT = '/usr/bin/wex'
CORE_BIN_FILE_LOCAL = '/usr/local/bin/wex'
CORE_COMMAND_NAME = 'wex'
FILE_README = 'README.md'
FILE_REGISTRY = 'registry.yml'
FILE_VERSION = 'version.txt'
GITHUB_GROUP = 'wexample'
GITHUB_PROJECT = 'wex'
KERNEL_RENDER_MODE_CLI = 'cli'
KERNEL_RENDER_MODE_COMMAND = 'command'
PASSWORD_INSECURE = 'thisIsAReallyNotSecurePassword!'
PYTHON_MIN_VERSION = (3, 10)
OWNER_USERNAME = 'owner'
ROOT_USERNAME = 'root'
SYSTEM_SERVICES_PATH = '/etc/systemd/system/'
SYSTEM_WWW_PATH = '/var/www'
SYSTEM_HOSTS_PATH = '/etc/hosts'
SERVICE_DAEMON_NAME = 'wexd.service'
SERVICE_DAEMON_PATH = f'{SYSTEM_SERVICES_PATH}{SERVICE_DAEMON_NAME}'
VERBOSITY_LEVEL_QUIET = 0
VERBOSITY_LEVEL_DEFAULT = 1
VERBOSITY_LEVEL_MEDIUM = 2
VERBOSITY_LEVEL_MAXIMUM = 3
