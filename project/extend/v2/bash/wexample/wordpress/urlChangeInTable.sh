#!/usr/bin/env bash

wordpressUrlChangeInTableArgs() {
  _ARGUMENTS=(
    'new_url n "New url with trailing slash (ex: http://wexample.com/) " false'
    'old_url o "Old url with trailing slash (ex: http://wexample.com/) " false'
    'table t "Comma separated list of tables" true'
  )
}

wordpressUrlChangeInTable() {
  . .wex

  # If no new url defined, use local config.
  if [ "${NEW_URL}" = "" ];then
    . ${WEX_APP_CONFIG}
    # Do not use https to support local envs.
    NEW_URL="http://${DOMAIN_MAIN}"
  fi

  if [ "${OLD_URL}" = "" ];then
    # Change database records.
    OLD_URL=$(wex db/exec -c="SELECT option_value FROM ${WP_DB_TABLE_PREFIX}options WHERE option_name = 'siteurl'")
  fi

  local QUERIES
  local SAVEIFS
  local TABLES

  # Allow multiple tables.
  TABLES=$(wex string/split -t="${TABLE}" -s=,)

  for TABLE in ${TABLES[*]}
  do
    TABLE=${WP_DB_TABLE_PREFIX}${TABLE}

    _wexLog "${WEX_COLOR_YELLOW}[${TABLE}]${WEX_COLOR_RESET} Search / Replace ${OLD_URL} by ${NEW_URL}"

    QUERIES=$(wex db/exec -c="SELECT CONCAT('UPDATE ', table_name, ' SET ', column_name, ' = REPLACE(', column_name, ', ''${OLD_URL}'', ''${NEW_URL}'');') FROM information_schema.columns WHERE table_name = '${TABLE}' AND (DATA_TYPE = 'longtext' OR DATA_TYPE = 'mediumtext' OR DATA_TYPE = 'text' OR DATA_TYPE = 'tinytext' OR DATA_TYPE = 'varchar');")

    SAVEIFS=${IFS}   # Save current IFS
    IFS=$'\n'      # Change IFS to new line
    QUERIES=( ${QUERIES} ) # Do not wrap with quotes
    IFS=${SAVEIFS}   # Restore IFS

    for (( I=0; I<${#QUERIES[@]}; I++ ))
    do
        _wexLog "SQL : ${QUERIES[$I]}"
        wex db/exec -c="${QUERIES[$I]}"
    done
  done;
}