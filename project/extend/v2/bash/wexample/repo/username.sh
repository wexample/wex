#!/usr/bin/env bash

repoUsername() {
  local REPO_USERNAME=$(wex var/localGet -n="REPO_USERNAME")

  if [ "${REPO_USERNAME}" == "" ];then
    local REPO_USERNAME=$(wex gitlab/get -p=user -k=username)
    wex var/localSet -n="REPO_USERNAME" -v=${REPO_USERNAME}
  fi

  echo ${REPO_USERNAME}
}
