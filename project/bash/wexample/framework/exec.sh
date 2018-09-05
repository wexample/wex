#!/usr/bin/env bash

frameworkExecArgs() {
  _ARGUMENTS=(
    [0]='command c "command to execute by detected framework(s)" true'
  )
}

frameworkExec() {
  # Per framework pull behavior.
  # Detect used frameworks
  FRAMEWORKS=($(wex framework/list -d=./project/))

  for FRAMEWORK in ${FRAMEWORKS[@]}
  do
    FRAMEWORK=framework$(wexUpperCaseFirstLetter ${FRAMEWORK})
    # Script exists : wexample::frameworkFwName/command
    if [ -f ${WEX_DIR_BASH}"wexample/"${FRAMEWORK}"/"${COMMAND}".sh" ];then
      wex wexample::${FRAMEWORK}/${COMMAND}
    fi
  done;
}