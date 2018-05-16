#!/usr/bin/env bash

serviceExecArgs() {
  _ARGUMENTS=(
    [0]='command c "Command name" true'
    [1]='service_only s "Service only" false'
    [2]='data d "Data" false'
  )
}

serviceExec() {
  SERVICES=($(wex service/list))
  COMMAND_UC=$(wexUpperCaseFirstLetter ${COMMAND})

  for SERVICE in ${SERVICES[@]}
  do
    if [ "${SERVICE_ONLY}" == "" ] || [ "${SERVICE_ONLY}" == "${SERVICE}" ];then
      SERVICE_DIR=${WEX_DIR_ROOT}"docker/services/"${SERVICE}"/"
      SERVICE_FILE_SCRIPT=${SERVICE_DIR}${COMMAND}".sh"

      if [[ -f ${SERVICE_FILE_SCRIPT} ]];then
        . ${SERVICE_FILE_SCRIPT}
        METHOD=${SERVICE}${COMMAND_UC}
        # Execute init method.
        ${METHOD} ${DATA}
      fi;
    fi
  done

}
