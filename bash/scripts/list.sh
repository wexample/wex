#!/usr/bin/env bash

scriptsListArgs() {
  _DESCRIPTION='List all scripts in a given directory'
  _ARGUMENTS=(
    'addon a "Addon name" false'
    'dir d "Directory (inside bash)" true'
  )
}

scriptsList() {
  local LIST
  local FIRST_LETTER
  local ADDON_PREFIX=""

  if [ "${ADDON}" != "" ];then
    ADDON_PREFIX="${ADDON}::"
  fi

  LIST=($(ls "${DIR}"))

  for GROUP in ${LIST[@]}
  do
    FIRST_LETTER="$(echo "${WEX_TEST_DIR_NAME}" | head -c 1)"
    if [ -d "${DIR}/${GROUP}" ] && [ "${FIRST_LETTER}" != "_" ]; then
      FILES=($(ls "${DIR}/${GROUP}"))

      for FILE in ${FILES[@]}
        do
          FIRST_LETTER="$(echo "${FILE}" | head -c 1)"

          if [[ "${FIRST_LETTER}" != "_" ]]; then
             echo "${ADDON_PREFIX}${GROUP}/${FILE%.*}"
          fi
      done
    fi
  done
}
