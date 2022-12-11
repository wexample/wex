#!/usr/bin/env bash

requirementsInstallArgs() {
  _DESCRIPTION='Install minimal requirements for a wex apps management.'
}

requirementsInstall() {
  case "$(wex system/os)" in
    "linux")
      wex package/update
      # First sudo package.
      apt-get install sudo -yq
      sudo apt-get install \
        git \
        net-tools \
        zip \
        -yq
      wex docker/install
      ;;
    "mac")
      # brew expect non root user.
      if [ $(whoami) == "root" ];then
        _wexError "Unable to install requirements as root user"
        exit
      fi
      # brew itself should be installed manually by user.
      # realpath and may be also already installed, but we reinstall with coreutils
      brew install \
        coreutils \
        git \
        zip
      ;;
  esac
}