#!/usr/bin/env bash

dbRestoreArgs() {
  _ARGUMENTS=(
    [0]='dump d "Dump file to import, in the dumps folder only, asked if missing" false'
  )
}

dbRestore() {
  # We expect to be into site root folder.

  # This may be improved in the future.
  CONTAINER_PATH_ROOT="/var/www/html"
  CONTAINER_PATH_DUMPS="/var/dumps"

  if [[ $(wex docker/isEnv) == false ]]; then

    # Ask user to choose a file.
    # Prompt does not work in the exec terminal.
    if [ -z ${DUMP+x} ];then
      FILES=($(ls dumps))

      if [[ ${#FILES[@]} == 0 ]];then
        echo "No dump found."
        return
      fi;

      echo ""
      # iterate through array using a counter
      for ((i=0; i<${#FILES[@]}; i++)); do
          echo -e "\t (${i}) ${FILES[$i]}"
      done
      echo ""

      while true; do
        read -p "Choose a dump to restore : " ANSWER
        if [ ${FILES[${ANSWER}]} ];then
          DUMP=${FILES[${ANSWER}]}
          break;
        fi;
      done
    fi;

    # Container should contain wexample script installed.
    wex site/exec -c="wex wexample::db/restore -d=${DUMP}"

  else
    # Go to site root.
    # It enables wexample site context.
    cd ${CONTAINER_PATH_ROOT}

    # Load env name.
    wex site/loadEnv

    # Can't load this data into container.
    . ${WEX_WEXAMPLE_SITE_CONFIG}

    # Load credentials stored into config
    wex site/configLoad

    wex framework/settings -d=${CONTAINER_PATH_ROOT}

    # Restore
    wex framework/restore \
      -f=${CONTAINER_PATH_DUMPS}"/"${DUMP} \
      -H=${SITE_NAME}"_mysql" \
      -P=${SITE_DB_PORT} \
      -db=${SITE_DB_NAME} \
      -u=${SITE_DB_USER} \
      -p=${SITE_DB_PASSWORD}
  fi
}
