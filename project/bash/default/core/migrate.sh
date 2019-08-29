#!/usr/bin/env bash

coreMigrateArgs() {
  _DESCRIPTION="Execute migrations"
  _ARGUMENTS=(
    [0]='from f "From version" true'
    [1]='to t "To version" true'
    [2]='command c "Command to execute" true'
  )
}

coreMigrate() {
  # Stop if no migration needed.
  if [ "${FROM}" == "${TO}" ];then
    return
  fi

  . ${WEX_DIR_BASH}/colors.sh
  local WEX_DIR_MIGRATION=${WEX_DIR_ROOT}"migration/"
  local COMMAND_LONG=_wexMigrate$(_wexUpperCaseFirstLetter ${COMMAND})

  _wexMigrateVersionSort() {
    printf "${1}" | sort -t '.' -k 1,1 -k 2,2 -k 3,3 -g
  }

  # Sort versions
  local MIGRATIONS="$(ls ${WEX_DIR_MIGRATION})"
  # Sort by version numbers
  MIGRATIONS=$(_wexMigrateVersionSort "${MIGRATIONS[@]}")

  for VERSION in ${MIGRATIONS}; do
      # Exclude .sh extension
      local VERSION_NUMBER=${VERSION::-3}
      local SORTED_LOW=($(_wexMigrateVersionSort "${VERSION_NUMBER}\n${FROM}"))
      local SORTED_HIGH=($(_wexMigrateVersionSort "${VERSION_NUMBER}\n${TO}"))

      # Reset command.
      unset -f ${COMMAND_LONG}

      # The number is greater than version CURRENT.
      # And the number is lower than version NEW.
      if [ ${SORTED_LOW[0]} == ${FROM} ] && [ ${SORTED_HIGH[0]} == ${VERSION_NUMBER} ];then
        . ${WEX_DIR_MIGRATION}${VERSION}

        if [[ $(type -t "${COMMAND_LONG}" 2>/dev/null) == function ]]; then
          _wexMessage "Updating to ${VERSION}" "Executing ${COMMAND} migration ..."
          # Execute command
          ${COMMAND_LONG}
        fi;
      fi
  done
}
