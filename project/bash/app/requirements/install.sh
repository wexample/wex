#!/usr/bin/env bash

requirementsInstallArgs() {
  _DESCRIPTION='Install minimal requirements for a wex apps management.'
}

requirementsInstall() {
  case "$(wex system/osName)" in
    "linux")
      apt-get install zip -yq
      wex docker/install
      ;;
  esac
}