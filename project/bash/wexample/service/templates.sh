#!/usr/bin/env bash

serviceTemplatesArgs() {
  _ARGUMENTS=(
    [0]='section s "Section name, must be a folder name also" true'
    [1]='extension e "Extension for file" false'
  )
}

serviceTemplates() {
  FOLDER="./"${SECTION}
  SECTION_FILES=$(ls ${FOLDER})
  FOUND=()

  # Get site env name.
  . .env

  for FILE in ${SECTION_FILES[@]};do
    SPLIT=($(wex text/split -s="." -t=${FILE}))
    BASE_NAME=${SPLIT[0]}

    # One execution only by base name,
    # Search for file variations inside it.
    if [[ $(wex array/contains -a="${FOUND[@]}" -i=${BASE_NAME}) == false ]];then
      # Save as found
      FOUND+=(${BASE_NAME})
      EXT_ENV=${SPLIT[@]:1}

      # Extension found
      if [[ ! -z "${EXT_ENV:+x}" ]];then
        EXT_ENV="."${EXT_ENV}
      fi

      FILE_ENV=${SPLIT[0]}"."${SITE_ENV}${EXT_ENV}

      # There is more than two pieces,
      # And second piece is env name, ex container.local.ext
      if [[ -f "./"${FOLDER}"/"${FILE_ENV} ]];then
        FILE=${FILE_ENV}
        # Remove env name
        CONF_VAR_BASE=${SPLIT[0]}" "${SPLIT[@]:1}
      # Base file ex container.ext
      else
        CONF_VAR_BASE=${SPLIT[@]}
      fi

      # Return to array
      CONF_VAR_BASE=(${CONF_VAR_BASE})
      # Append folder name in second position
      CONF_VAR_BASE="${CONF_VAR_BASE[0]} ${SECTION} ${CONF_VAR_BASE[@]:1}"
      CONF_VAR_BASE=$(wex array/join -a="${CONF_VAR_BASE}" -s="_")
      CONF_VAR_BASE=$(wex text/uppercase -t=${CONF_VAR_BASE})

      # Not already found.
      echo "\nCONF_"${CONF_VAR_BASE}'='$(realpath ${FOLDER}'/'${FILE})
    fi
  done
}
