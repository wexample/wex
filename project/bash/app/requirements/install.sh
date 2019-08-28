#!/usr/bin/env bash

requirementsInstallArgs() {
  _DESCRIPTION='Install minimal requirements for a wex apps management.'
}

requirementsInstall() {
  case "$(wex system/osName)" in
    "linux")
      wex package/update
      wex docker/install
      sudo apt-get install \
        ansible \
        git \
        zip \
        -yq
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
        ansible \
        coreutils \
        git \
        zip \
        -yq
      ;;
  esac
}