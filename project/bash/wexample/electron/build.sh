#!/usr/bin/env bash

electronBuildArgs() {
  _ARGUMENTS=(
    [0]='reload r "Clear electron binaries and download it again" false'
  )
}

electronBuild() {
  # Clear old dist
  rm -rf ./dist
  rm -rf ./installer

  cd ./project/
  # Using electron-builder
  yarn dist
  # Expected LICENSE file.
  cp ./LICENSE ./dist/win-unpacked/LICENSE
  # Using electron/windows-installer
  # TODO TEMP, find a way to execute localized node script
  node _temp_electron_installer.js
}
