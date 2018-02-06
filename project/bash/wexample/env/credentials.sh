#!/usr/bin/env bash

envCredentialsArgs() {
  _ARGUMENTS=(
    [0]='ssj_username u "SSH Username" false'
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
    VAR_NAME=DB_REMOTE_$(wex text/uppercase -t=${ENVIRONMENT})_SSH_USERNAME
    SITE_USERNAME=$(wex env/readVar -l="SSH Username for ${ENVIRONMENT}" -k=${VAR_NAME} -d=root ${COMMAND_OPTIONS})
  fi

  # Private key specified
  if [ ! -z "${PRIVATE_KEY:+x}" ]; then
    SITE_PRIVATE_KEY=${PRIVATE_KEY}
  else
    # SSH Private key
    VAR_NAME=DB_REMOTE_$(wex text/uppercase -t=${ENVIRONMENT})_SSH_PRIVATE_KEY
    SITE_PRIVATE_KEY=$(wex env/readVar -l="SSH Private key for : ${ENVIRONMENT}" -k=${VAR_NAME} -d=root ${COMMAND_OPTIONS})
  fi

  # Script may be executed in an environment
  # with no .env file (ie CI)
  if [ -z ${ENVIRONMENT+x} ];then
    # Get site env.
    . ${DIR_SITE}.env
  fi

  # Conf contains site name
  export SITE_USERNAME=${SITE_USERNAME};
  export SITE_PRIVATE_KEY=${SITE_PRIVATE_KEY};
  export SITE_IPV4=$(wex json/readValue -f=${DIR_SITE}wex.json -k=${ENVIRONMENT}.ipv4)
  export SITE_PORT=$(wex json/readValue -f=${DIR_SITE}wex.json -k=${ENVIRONMENT}.port)
  # We may set it somewhere else.
  export SITE_PATH_ROOT=/var/www/${SITE_NAME}/
}
