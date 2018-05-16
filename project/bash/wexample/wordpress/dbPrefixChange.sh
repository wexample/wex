#!/usr/bin/env bash

wordpressDbPrefixChangeArgs() {
  _ARGUMENTS=(
    [0]='old_prefix o "Old prefix" true'
    [1]='new_prefix n "New prefix" false'
  )
}

# Remove a prefix, do not execute twice !
wordpressDbPrefixChange() {
  local TABLES=$(wex db/exec -c="SHOW TABLES;" -o="-B");
  local PREFIX_LENGTH=${#OLD_PREFIX}

  for TABLE in ${TABLES[@]}
  do
    # Double [[]] is required for advanced comparison.
    if [[ "${TABLE}" != Tables_in_* ]];then
      local QUERY='RENAME TABLE '${TABLE}' TO '${NEW_PREFIX}${TABLE:${PREFIX_LENGTH}}
      wex db/exec -c="${QUERY}"
    fi
  done
}