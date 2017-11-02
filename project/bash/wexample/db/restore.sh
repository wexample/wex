#!/usr/bin/env bash

dbRestoreArgs() {
  _ARGUMENTS=(
    [0]='site_name n "Website name (internal usage for container execution)" false'
    [1]='site_env e "Website environment (internal usage for container execution)" false'
    [2]='dump d "Dump file to import, in the dumps folder only, asked if missing" false'
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

    # Load env name.
    wex site/loadEnv
    # Can't load this data into container.
    SITE_NAME=$(wex site/config -k=name)
    # Container should contain wexample script installed.
    wex site/exec -c="wex wexample::db/restore -n=${SITE_NAME} -e=${SITE_ENV} -d=${DUMP}"

  else
    # In this section we can't use wexample sites specific methods
    # We have to pass arguments for host call if needed.

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
