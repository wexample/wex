#!/usr/bin/env bash

frameworkDumpArgs() {
  _ARGUMENTS=(
    [0]='dump_dir d "Target directory for dumps" true'
    [1]='prefix px "Prefix for final file" false'
    [2]='zip zip "Use ZIP" false'
    [3]='zip_only zo "Remove original file after ZIP it" false'
    [4]='host h "Database host server" false'
    [5]='port p "Database host port" false'
    [6]='database db "Database name" false'
    [7]='user u "Database username" false'
    [8]='suffix sx "Suffix for final file" false'
  )
}

frameworkDump() {
  # Build dump name.
  DUMP_FILE_NAME=${PREFIX}${DATABASE}"-"$(wex date/timeFileName)${SUFFIX}".sql"
  DUMP_FULL_PATH=${DUMP_DIR}"/"${DUMP_FILE_NAME}

  mysqldump $(wex mysql/loginCommand) > ${DUMP_FULL_PATH}

  if [[ ${ZIP} == true ]]; then
    zip ${DUMP_FULL_PATH}".zip" ${DUMP_FULL_PATH} -q -j

    # Expect only zipped file
    # Remove original.
    if [ ! -z "${ZIP_ONLY+x}" ]; then
      rm -rf ${DUMP_FULL_PATH}
      # Return the zipped file name.
      echo ${DUMP_FULL_PATH}".zip"
      return
    fi;
  fi

  # Return dump file name.
  echo ${DUMP_FULL_PATH}
}
