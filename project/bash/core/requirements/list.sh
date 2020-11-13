#!/usr/bin/env bash

requirementsListArgs() {
  _DESCRIPTION='Display installed requirement for some wex features'
}

requirementsList() {
  . ${WEX_DIR_BASH}colors.sh

  local OS_NAME=$(wex system/osName)

  # Keep alphabetical order for all os.
  # Think to update also wex requirements/installed if list changes.
  _requirementsListRow $(wex package/exists -n ansible) "ansible\t\t" "Servers management and orchestration"
  [ "${OS_NAME}" == "mac" ] && _requirementsListRow $(wex package/exists -n brew) "brew\t\t" "Package manager"
  _requirementsListRow $(wex package/exists -n docker) "docker\t\t" "Containers manager"
  _requirementsListRow $(wex package/exists -n git) "git\t\t" "Version control"
  _requirementsListRow $(wex package/exists -n ifconfig) "ifconfig\t" "Network interface configuration"
  [ "${OS_NAME}" == "mac" ] && _requirementsListRow $(_wexHasRealPath == "true") "realpath\t" "Base bash method"
  _requirementsListRow $(wex package/exists -n sudo) "sudo\t\t" "Super user access"
  _requirementsListRow $(wex package/exists -n zip) "zip\t\t" "Used for backups management"
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

  printf "   "${ICON}${WEX_COLOR_RESET}"\t${NAME}${WEX_COLOR_CYAN}${DESC}${WEX_COLOR_RESET}\n"
}