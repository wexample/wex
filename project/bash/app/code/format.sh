#!/usr/bin/env bash

codeFormatArgs() {
  _DESCRIPTION="Launch the code formating command for the app"
  _ARGUMENTS=(
    [0]='commit c "Commit changes" false'
  )
}

codeFormat() {
  wex hook/exec -c=codeFormat

  if [ "${COMMIT}" != "" ];then
    # Go to the project folder in case of root dir
    # has not the same git repo as the project content.
    cd ${WEX_WEXAMPLE_APP_DIR_PROJECT}

    git commit -am "Code auto format"
  fi
}