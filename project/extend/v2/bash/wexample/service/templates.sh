#!/usr/bin/env bash

serviceTemplatesArgs() {
  _ARGUMENTS=(
    [0]='section s "Section name, can be a folder name" true'
    [1]='extension e "Extension for file" false'
  )
}

serviceTemplates() {
  FOLDER="./"${SECTION}
  SECTION_FILES=$(ls ${FOLDER})
  local NAMES_PROCESSED=()

  # Get site env name.
  local SITE_ENV=$(wex site/env)

  for FILE in ${SECTION_FILES[@]};do
    SPLIT=($(wex text/split -s="." -t=${FILE}))
    BASE_NAME=${SPLIT[0]}

    # Base file ex container.ext
    local CONF_VAR_NAME=${SPLIT[@]}
    local IS_ENV=false

    # There is more than two pieces
    if [ "${SPLIT[2]}" != "" ];then
      local IS_ENV=true
      # Second part si equal to
      if [ "${SPLIT[1]}" == ${SITE_ENV} ];then
        # Remove env name
        CONF_VAR_NAME=${SPLIT[0]}" "${SPLIT[2]}
        # This is an unexpected.name.ext
      else
        CONF_VAR_NAME=false
      fi
    fi

    # One execution only by base name,
    # Search for file variations inside it.
    # Allow to write same variable twot time if env file is found after generic one.
    if [ "${CONF_VAR_NAME}" != false ] && ([[ ! " ${NAMES_PROCESSED[@]} " =~ " ${SPLIT[0]} " ]] || [ ${IS_ENV} == true ]);then
      # Save as found
      NAMES_PROCESSED+=(${SPLIT[0]})

      # Return to array
      CONF_VAR_NAME=(${CONF_VAR_NAME})
      # Append folder name in second position
      CONF_VAR_NAME="${SPLIT[0]} ${SECTION} ${CONF_VAR_NAME[@]:1}"
      CONF_VAR_NAME=$(wex array/join -a="${CONF_VAR_NAME}" -s="_")
      CONF_VAR_NAME=${CONF_VAR_NAME^^}

     # Not already found.
      echo "\nCONF_"${CONF_VAR_NAME}'='$(realpath ${FOLDER}'/'${FILE})
    fi
  done
}
