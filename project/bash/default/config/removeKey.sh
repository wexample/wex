#!/usr/bin/env bash

configRemoveKeyArgs() {
  _ARGUMENTS=(
    [0]='target_key k "Target key to get (line beginning by ... regex)" true'
    [1]='file f "File" true'
  )
}

configRemoveKey() {
  sed -i '/^[ ]\{0,\}'${TARGET_KEY}'/d' ${FILE}
}
