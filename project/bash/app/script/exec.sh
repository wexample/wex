#!/usr/bin/env bash

scriptExecArgs() {
  _ARGUMENTS=(
<<<<<<<< HEAD:project/bash/app/script/exec.sh
    'command c "Command name, ex : "command" to execute ci/command.sh" true'
========
    [0]='command c "Command name, ex : "command" to execute ci/command.sh" true'
    [1]='args a "Arguments to pass to script, ex "foo=bar"" false'
>>>>>>>> master:project/extend/v2/bash/wexample/script/exec.sh
  )
}

scriptExec() {
  local FILE_PATH=script/${COMMAND}.sh

  # Execute custom script for site.
  if [ -f ${FILE_PATH} ];then
    . ${FILE_PATH} ${ARGS}
  fi
}
