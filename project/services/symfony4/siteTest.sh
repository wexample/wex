#!/usr/bin/env bash

symfony4SiteTest() {
  local ARGS='';

  # File is based form root in order to allow user to use auto-complete
  if [ "${TEST_FILE}" != '' ];then
    local ARGS='../'${TEST_FILE}

    if [ "${TEST_METHOD}" != '' ];then
      local ARGS=' --filter '${TEST_METHOD}' '${ARGS}
    fi;
  fi;

  wex site/exec -c="cd /var/www/html/project && ./bin/phpunit ${ARGS}"
}