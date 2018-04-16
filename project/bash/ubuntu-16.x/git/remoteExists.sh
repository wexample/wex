#!/usr/bin/env bash

gitRemoteExistsArgs() {
  _ARGUMENTS=(
    [0]='repo r "Repo url" true'
  )
}

gitRemoteExists() {
  git ls-remote "${REPO}" -h --exit-code &> /dev/null;
  # Get exit code
  local EXIT_CODE=$(echo $?)

  if [ "${EXIT_CODE}" == 128 ];then
    echo false
  else
    echo true
  fi
}
