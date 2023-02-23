#!/usr/bin/env bash

scriptsListArgs() {
  # shellcheck disable=SC2034
  _DESCRIPTION='List all scripts in a given directory'
  # shellcheck disable=SC2034
  _ARGUMENTS=(
    'addon a "Addon prefix" false'
    'dir d "Directory (inside bash)" true'
    'filepath f "Return also script file path false false"'
  )
}

scriptsList() {
  local LIST
  local FIRST_LETTER

  if [ ! -d "${DIR}" ];then
    return
  fi

  if [ "${ADDON}" != "" ];then
    ADDON="${ADDON}::"
  fi

  LIST=($(ls "${DIR}"))

  for GROUP in ${LIST[@]}
  do
    FIRST_LETTER="$(echo "${GROUP}" | head -c 1)"
    if [ -d "${DIR}/${GROUP}" ] && [ "${FIRST_LETTER}" != "_" ]; then
      FILES=($(ls "${DIR}/${GROUP}"))

      for FILE in ${FILES[@]}
        do
          FIRST_LETTER="$(echo "${FILE}" | head -c 1)"

          if [[ "${FIRST_LETTER}" != "_" ]]; then
             local OUTPUT="${ADDON}${GROUP}/${FILE%.*}"

             if [[ ${FILEPATH} == true ]];then
               OUTPUT="${OUTPUT}#${DIR}${GROUP}/${FILE}"
             fi

             echo "${OUTPUT}"
          fi
      done
    fi
  done
}
