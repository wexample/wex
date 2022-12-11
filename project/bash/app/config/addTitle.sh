#!/usr/bin/env bash

configAddTitleArgs() {
  _ARGUMENTS=(
    'title t "Title text" true'
  )
}

configAddTitle() {
  echo -e "\n\n# ${TITLE}" >> "${WEX_WEXAMPLE_APP_FILE_CONFIG}"
}
