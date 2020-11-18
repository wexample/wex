#!/usr/bin/env bash

sshKeySelectListArgs() {
  _ARGUMENTS=(
    [0]='public pub "Public key" false'
  )
}

sshKeySelectList() {
  # Find local key.
  local HOME_DIR=$(wex user/homeDir)
  local USERS_DIRS=($(ls ${HOME_DIR}))
  local KEYS_AVAILABLE=(${CUSTOM_PATH_LABEL});
  local COUNT=1

  echo -e "\t (${COUNT}) <CustomPath>"
  ((COUNT++))

  for USER_NAME in ${USERS_DIRS[@]}
  do
    local KEYS_DIR=${HOME_DIR}${USER_NAME}/.ssh/
    if [ -d ${KEYS_DIR} ];then
      local KEYS=($(ls ${KEYS_DIR}))
      for KEY in ${KEYS[@]}
      do
        if ([ "${PUBLIC}" != true ] && [ "${KEY##*.}" != "pub" ]) || ([ "${PUBLIC}" == "true" ] && [ "${KEY##*.}" == "pub" ]);then
          echo -e "\t (${COUNT}) ${KEYS_DIR}${KEY}"
          ((COUNT++))
        fi
      done;
    fi
  done;
}
