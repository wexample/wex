#!/usr/bin/env bash

cliExecArgs() {
  _ARGUMENTS=(
    [0]='command c "Command to execute" false'
  )
}

# This methods should handle all "cli" tools for current website,
# it have to be able to detect site framework and use proper cli tool
cliExec() {
  # Silex
  wex site/exec -c="cd /var/www/html/project && php app/console ${COMMAND}"
}