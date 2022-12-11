#!/usr/bin/env bash

repoName() {
  local REPO_NAME=$(wex var/localGet -n="REPO_NAME")

  if [ "${REPO_NAME}" == "" ];then
    # Load site name.
    wex config/load --quiet
    local REPO_NAMESPACE=$(wex repo/namespace)
    # Encode name
    REPO_NAME=$(wex url/encode -t="${REPO_NAMESPACE}/${SITE_NAME}")
    # Save.
    wex var/localSet -n="REPO_NAME" -v=${REPO_NAME}
  fi

  echo ${REPO_NAME}
}
