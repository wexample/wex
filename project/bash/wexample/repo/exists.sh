#!/usr/bin/env bash

repoExists() {
  local REPO_NAME=$(wex repo/name)
  local BASE_URL=$(wex gitlab/baseUrl -p="projects/"${REPO_NAME})
  local RESPONSE_CODE=$(curl -s -o /dev/null -w "%{http_code}" ${BASE_URL})
  # Check response code.
  if [ ${RESPONSE_CODE} == 200 ];then
    echo true
  else
    echo false
  fi
}
