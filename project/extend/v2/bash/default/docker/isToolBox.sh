#!/usr/bin/env bash

dockerIsToolBox() {
  if [ "${DOCKER_TOOLBOX_INSTALL_PATH}" ];then
    echo true
  else
    echo false
  fi
}
