#!/usr/bin/env bash

configWriteArgs() {
  _AS_NON_SUDO=false
  _ARGUMENTS=(
    'started s "Set the site is started or not" false'
    'no_recreate nr "No recreate if files exists" false'
  )
}

configWrite() {

  # No recreate.
  if [ "${NO_RECREATE}" == true ] &&
    [ -f ${WEX_WEXAMPLE_APP_DIR_TMP}config ] &&
    [ -f ${WEX_WEXAMPLE_APP_COMPOSE_BUILD_YML} ];then
    return
  fi

  # TODO finish migration
  sudo ${WEX_DIR_ROOT}extend/v2/bash/wex config/write ${@}
}
