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
echo "a"
  COMMAND_OPTIONS=" --ask=${NON_INTERACTIVE} --write=${NON_INTERACTIVE}"

echo "b"
  # Username specified
  if [ ! -z "${SSH_USERNAME:+x}" ];then
  echo "c"
    SITE_USERNAME=${SSH_USERNAME}
  else
  echo "d"
    # Username
    VAR_NAME=DB_REMOTE_$(wex text/uppercase -t=${ENVIRONMENT})_SSH_USERNAME
    SITE_USERNAME=$(wex env/readVar -l="SSH Username for ${ENVIRONMENT}" -k=${VAR_NAME} -d=root ${COMMAND_OPTIONS})
  fi
echo "e"
  # Private key specified
  if [ ! -z "${PRIVATE_KEY:+x}" ]; then
  echo "f"
    SITE_PRIVATE_KEY=${PRIVATE_KEY}
  else
  echo "g"
    # SSH Private key
    VAR_NAME=DB_REMOTE_$(wex text/uppercase -t=${ENVIRONMENT})_SSH_PRIVATE_KEY
    SITE_PRIVATE_KEY=$(wex env/readVar -l="SSH Private key for : ${ENVIRONMENT}" -k=${VAR_NAME} -d=root ${COMMAND_OPTIONS})
  fi

echo "g"
  # We can't use `wex site/configLoad`
  # because it need te rewriting configuration with docker.
  SITE_NAME=$(wex site/config -k=name)
echo "h"
  if [ ! -z ${ENVIRONMENT+x} ];then
    echo "i"
    # Get site env.
    . ${DIR_SITE}.env
  fi

echo "j"
  # Conf contains site name
  export SITE_NAME=${SITE_NAME};
  export SITE_USERNAME=${SITE_USERNAME};
  export SITE_PRIVATE_KEY=${SITE_PRIVATE_KEY};
  export SITE_IPV4=$(wex json/readValue -f=${DIR_SITE}wex.json -k=${ENVIRONMENT}.ipv4)
  export SITE_PORT=$(wex json/readValue -f=${DIR_SITE}wex.json -k=${ENVIRONMENT}.port)
  # We may set it somewhere else.
  export SITE_PATH_ROOT=/var/www/${SITE_NAME}/
}
