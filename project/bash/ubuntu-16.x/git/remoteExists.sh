#!/usr/bin/env bash

gitRemoteExistsArgs() {
  _ARGUMENTS=(
<<<<<<< HEAD
    [0]='repo r "Repository url" true'
=======
    [0]='repo r "Repo url" true'
>>>>>>> a42e0c71b05f3b511fdadcb43ce0b8384d2fd654
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
