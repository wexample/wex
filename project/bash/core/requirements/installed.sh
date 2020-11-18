#!/usr/bin/env bash

requirementsInstalledArgs() {
  _DESCRIPTION='Return true if all requirements are installed'
}

requirementsInstalled() {
  # Think to update also wex requirements/list if list changes.
  if [[ $(wex package/exists -n docker) == false ]] ||
     [[ $(wex package/exists -n zip) == false ]];then
    echo "false"
  else
    echo "true"
  fi
}