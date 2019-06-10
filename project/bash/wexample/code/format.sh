#!/usr/bin/env bash

codeFormatArgs() {
  _ARGUMENTS=(
    [0]='commit c "Commit changes" false'
  )
}

codeFormat() {
  wex hook/exec -c=codeFormat

  if [ "${COMMIT}" != "" ];then
    git commit -am "Code auto format"
  fi
}