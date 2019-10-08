#!/usr/bin/env bash

wordpressDbPrefixChangeArgs() {
  _ARGUMENTS=(
    [0]='old_prefix o "Old prefix" true'
    [1]='new_prefix n "New prefix" false'
  )
}

# Remove a prefix, do not execute twice !
wordpressDbPrefixChange() {
  local TABLES=$(wex db/exec -c="SHOW TABLES;");
  local PREFIX_LENGTH=${#OLD_PREFIX}

  for TABLE in ${TABLES[@]}
  do
    # Double [[]] is required for advanced comparison.
    if [[ "${TABLE}" != Tables_in_* ]];then
      local QUERY='RENAME TABLE '${TABLE}' TO '${NEW_PREFIX}${TABLE:${PREFIX_LENGTH}}
      wex db/exec -c="${QUERY}"
    fi
  done

  local IDS=($(wex db/exec -c="SELECT umeta_id FROM ${NEW_PREFIX}usermeta WHERE meta_key LIKE '"${OLD_PREFIX}"%';"))
  local NAMES=($(wex db/exec -c="SELECT meta_key FROM ${NEW_PREFIX}usermeta WHERE meta_key LIKE '"${OLD_PREFIX}"%';"))
  local COUNT=0

  for NAME in ${NAMES[@]}
  do
    local QUERY="UPDATE usermeta SET meta_key = '${NAME:${PREFIX_LENGTH}}' WHERE umeta_id = '${IDS[${COUNT}]}'"
    wex db/exec -c="${QUERY}"
    (( COUNT++ ))
  done
}