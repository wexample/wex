#!/usr/bin/env bash

requirementsInstallArgs() {
  _DESCRIPTION='Install minimal requirements for a wex.'
}

requirementsInstall() {
  case "$(wex system/os)" in
    "linux")
      apt-get install git -yq
      ;;
  esac
}