#!/usr/bin/env bash

requirementsListArgs() {
  _DESCRIPTION='Display installed requirement for some wex features'
}

requirementsList() {
  . ${WEX_DIR_BASH}colors.sh

  # Think to update also wex requirements/installed if list changes.
  _requirementsListRow $(wex package/exists -n ansible) "ansible" "Servers management and orchestration"
  _requirementsListRow $(wex package/exists -n docker) "docker" "Core containers manager"
  _requirementsListRow $(wex package/exists -n zip) "zip" "Use for backups management"
}

_requirementsListRow() {
  local EXISTS=${1}
  local NAME=${2}
  local DESC=${3}

  if [ "${EXISTS}" == "true" ];then
    local ICON="${WEX_COLOR_GREEN}✓"
  else
    local ICON=${WEX_COLOR_RED}x
  fi

  printf "   "${ICON}${WEX_COLOR_RESET}"\t${NAME}\t\t${WEX_COLOR_CYAN}${DESC}${WEX_COLOR_RESET}\n"
}