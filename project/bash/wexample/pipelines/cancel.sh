#!/usr/bin/env bash

# Cancel all running pipelines.
pipelinesCancel() {
  local LINE=''
  local REPO_NAME=$(wex repo/name);

  while : ; do
    # Get all pipelines
    local PIPELINES_JSON=$(wex wexample::gitlab/get -p="projects/wexample%2fping/pipelines")
    # Search for one which is not stopped.
    local PIPELINE_ACTIVE_ID=$(wex json/search -k=id -s=status -v=running -j=${PIPELINES_JSON})
    # No more running.
    if [ "${PIPELINE_ACTIVE_ID}" == "" ];then
      return
    fi
    # Stops occurs immediately.
    wex wexample::gitlab/post -p="projects/${REPO_NAME}/pipelines/"${PIPELINE_ACTIVE_ID}"/cancel"
  done
}