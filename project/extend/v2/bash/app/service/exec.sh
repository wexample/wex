#!/usr/bin/env bash

serviceExecArgs() {
  _ARGUMENTS=(
    [0]='command c "Command name" true'
    [1]='service_only s "Service only" false'
    [2]='service_only_forced sf "Force to use service even not registered into site config" false'
    [3]='data d "Data" false'
    [4]='parse p "Parse output variables" false'
    [5]='no_wrap nw "Do not catch output into variable (should be the future recomended usage)" false'
  )
}

serviceExec() {
  # Service name specified.
  if [ "${SERVICE_ONLY}" != "" ] && [ "${SERVICE_ONLY_FORCED}" == true ];then
    local SERVICES=(${SERVICE_ONLY})
  else
    local SERVICES=($(wex service/list))
  fi

  local COMMAND_BASE="${COMMAND}"
  local COMMAND_UC=$(wexUpperCaseFirstLetter ${COMMAND_BASE})
  local OUTPUT=''

  for SERVICE in "${SERVICES[@]}"
  do
    if [ "${SERVICE_ONLY}" == "" ] || [ "${SERVICE_ONLY}" == "${SERVICE}" ];then
      SERVICE_DIR=${WEX_DIR_ROOT}"services/"${SERVICE}"/"
      SERVICE_FILE_SCRIPT=${SERVICE_DIR}${COMMAND_BASE}".sh"

      if [ -f "${SERVICE_FILE_SCRIPT}" ];then
        . ${SERVICE_FILE_SCRIPT}
        METHOD=${SERVICE}${COMMAND_UC}
        if [ "${NO_WRAP}" == "" ];then
          # Execute init method.
          OUTPUT+=$(${METHOD} ${DATA})
        else
          # Execute init method.
          ${METHOD} ${DATA}
        fi;
      fi;
    fi
  done

  echo ${OUTPUT}
}
