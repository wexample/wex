#!/usr/bin/env bash

serviceExecArgs() {
  _ARGUMENTS=(
    'command c "Command name" true'
    'service_only s "Service only" false'
    'service_only_forced sf "Force to use service even not registered into site config" false'
    'data d "Data" false'
    'parse p "Parse output variables" false'
  )
}

serviceExec() {
  # Service name specified.
  if [ "${SERVICE_ONLY}" != "" ] && [ "${SERVICE_ONLY_FORCED}" == true ];then
    local SERVICES=(${SERVICE_ONLY})
  else
    local SERVICES=($(wex service/list))
  fi

  COMMAND_UC=$(_wexUpperCaseFirstLetter ${COMMAND})

  for SERVICE in ${SERVICES[@]}
  do
    _wexLog "Executing ${SERVICE}${COMMAND_UC}"

    if [ "${SERVICE_ONLY}" == "" ] || [ "${SERVICE_ONLY}" == "${SERVICE}" ];then
      local SERVICE_DIR=${WEX_DIR_SERVICES}${SERVICE}"/"
      local SERVICE_FILE_SCRIPT=${SERVICE_DIR}${COMMAND}".sh"

      if [[ -f ${SERVICE_FILE_SCRIPT} ]];then
        . ${SERVICE_FILE_SCRIPT}
        local METHOD=${SERVICE}${COMMAND_UC}

        ${METHOD} ${DATA}
      fi;
    fi
  done
}
