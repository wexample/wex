#!/usr/bin/env bash

requirementsInstallArgs() {
  _DESCRIPTION='Install minimal requirements for a wex project to run locally.'
}

requirementsInstall() {
  case "$(wex system/osName)" in
    "linux")
      apt-get install zip -yq
      wex docker/install
      ;;
  esac
}