#!/usr/bin/env bash

repoNamespace() {
  local REPO_NAMESPACE=$(wex var/localGet -n="REPO_NAMESPACE")

  if [ "${REPO_NAMESPACE}" == "" ];then
    # Get username as default namespace.
    local GITLAB_USERNAME=$(wex gitlab/get -p=user -k=username)
    # Ask user to choice a custom namespace.
    REPO_NAMESPACE=$(wex var/localGet -r -n="REPO_NAMESPACE" -a="Please enter the repository namespace ?" -d=${GITLAB_USERNAME})
  fi

  echo ${REPO_NAMESPACE}
}
