#!/usr/bin/env bash

envCredentialsArgs() {
  _ARGUMENTS=(
    [0]='ssh_username u "SSH Username" false'
    [1]='private_key pk "SSH Private key" false'
    [2]='environment e "Environment to connect to" true'
    [3]='dir_site d "Local root site directory" false'
  )
}

envCredentials() {
  if [ -z "${DIR_SITE+x}" ]; then
    DIR_SITE=./
  fi;

  COMMAND_OPTIONS=" --ask=${NON_INTERACTIVE} --write=${NON_INTERACTIVE}"

  # Username specified
  if [ ! -z "${SSH_USERNAME:+x}" ];then
    SITE_USERNAME=${SSH_USERNAME}
  else
    # Username
    VAR_NAME=DB_REMOTE_${ENVIRONMENT^^}_SSH_USERNAME
    SITE_USERNAME=$(wex env/var -l="SSH Username for ${ENVIRONMENT}" -k=${VAR_NAME} -d=root ${COMMAND_OPTIONS})
  fi

  # Private key specified
  if [ ! -z "${PRIVATE_KEY:+x}" ]; then
    SITE_PRIVATE_KEY=${PRIVATE_KEY}
  else
    # SSH Private key
    VAR_NAME=DB_REMOTE_${ENVIRONMENT^^}_SSH_PRIVATE_KEY
    SITE_PRIVATE_KEY=$(wex env/var -l="SSH Private key for : ${ENVIRONMENT}" -k=${VAR_NAME} -d=root ${COMMAND_OPTIONS})
  fi

  # Script may be executed in an environment
  # with no .env file (ie CI)
  if [ -z ${ENVIRONMENT+x} ];then
    # Get site env.
    local ENVIRONMENT=$(wex site/env)
  fi

  . ${DIR_SITE}.wex

  # Conf contains site name
  export SITE_USERNAME=${SITE_USERNAME};
  export SITE_PRIVATE_KEY=${SITE_PRIVATE_KEY};
  export SITE_IPV4=${PROD_SSH_HOST}
  export SITE_PORT=${PROD_PORT}
  # We may set it somewhere else.
  export SITE_PATH_ROOT=${WEX_WEXAMPLE_DIR_SITES_DEFAULT}${NAME}/
}
