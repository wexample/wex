#!/usr/bin/env bash

pipelineReady() {
  local REPO_NAME=$(wex repo/name)
  local JSON=$(wex gitlab/get -p=projects/${REPO_NAME}/pipelines)
  local BLOCKING_STATUS=(running pending)

  for STATUS in ${BLOCKING_STATUS[@]};do
    local HAS_STATUS=$(echo ${JSON} | sed -E 's/^.\{0,\}\"status\"\:\"'${STATUS}'\".\{0,\}$/true/')
    if [ "${HAS_STATUS}" == true ];then
      echo false
      return
    fi
  done

  echo true
}