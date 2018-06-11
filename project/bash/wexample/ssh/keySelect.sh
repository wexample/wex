#!/usr/bin/env bash

sshKeySelectArgs() {
  _ARGUMENTS=(
    [0]='name n "SSH Key local name" false'
    [1]='description d "Description" true'
    [2]='public pub "Public key" false'
  )
}

sshKeySelect() {
  # Find local key.
  local HOME_DIR=$(wex user/homeDir)
  local USERS_DIRS=($(ls ${HOME_DIR}))
  local KEYS_AVAILABLE=()
  local CUSTOM_PATH_LABEL="<CustomPath>"
  local COUNT=0
  local SELECTED=""

  KEYS_AVAILABLE[${COUNT}]="${CUSTOM_PATH_LABEL}"
  COUNT=1

  for USER_NAME in ${USERS_DIRS[@]}
  do
    local KEYS_DIR=${HOME_DIR}${USER_NAME}/.ssh/
    if [ -d ${KEYS_DIR} ];then
      local KEYS=($(ls ${KEYS_DIR}))
      for KEY in ${KEYS[@]}
      do
        if ([ "${PUBLIC}" != true ] && [ "${KEY##*.}" != "pub" ]) || ([ "${PUBLIC}" == "true" ] && [ "${KEY##*.}" == "pub" ]);then
          KEYS_AVAILABLE+=("${KEYS_DIR}${KEY}")
          ((COUNT++))
        fi
      done;
    fi
  done;

  while true; do
    read -p "Type a number or the path of your custom key (1 to ${#KEYS_AVAILABLE[@]}) : " ANSWER
    ((ANSWER--))
    if [ ${KEYS_AVAILABLE[${ANSWER}]} ];then
      SELECTED=${KEYS_AVAILABLE[${ANSWER}]}
      break;
    fi;
  done

  # Saving expected
  if [ "${NAME}" != "" ]; then
    if [ ${SELECTED} == ${CUSTOM_PATH_LABEL} ];then
      # Clear
      wex wexample::var/localClear -n="${NAME}"
      SELECTED=$(wex wexample::var/localGet -n="${NAME}" -a="${DESCRIPTION}" -r)
    else
      $(wex wexample::var/localSet -n="${NAME}" -v="${SELECTED}")
    fi
  else
    echo ${SELECTED}
  fi
}
