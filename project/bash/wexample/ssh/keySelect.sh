#!/usr/bin/env bash

sshKeySelectArgs() {
  _ARGUMENTS=(
    [0]='name n "SSH Key local name" true'
    [1]='description d "Description" true'
  )
}

sshKeySelect() {
  # Find local key.
  local HOME_DIR=$(wex user/homeDir)
  local USERS_DIRS=($(ls ${HOME_DIR}))
  local CUSTOM_PATH_LABEL="<CustomPath>"
  local KEYS_AVAILABLE=(${CUSTOM_PATH_LABEL});

  for USER_NAME in ${USERS_DIRS[@]}
  do
    local KEYS_DIR=${HOME_DIR}${USER_NAME}/.ssh/
    if [ -d ${KEYS_DIR} ];then
      local KEYS=($(ls ${KEYS_DIR}))
      for KEY in ${KEYS[@]}
      do
        if [ "${KEY##*.}" != "pub" ];then
          KEYS_AVAILABLE+=("${KEYS_DIR}${KEY}")
        fi
      done;
    fi
  done;

  echo "Type a number or the path of your custom key"
  select SELECTED in ${KEYS_AVAILABLE[@]};
  do
    #
    if [ ${SELECTED} == ${CUSTOM_PATH_LABEL} ];then
      # Clear
      wex wexample::var/localClear -n="${NAME}"
      SELECTED=$(wex wexample::var/localGet -n="${NAME}" -a="${DESCRIPTION}" -r)
    else
      $(wex wexample::var/localSet -n="${NAME}" -v="${SELECTED}")
    fi
    break
  done
}
