#!/usr/bin/env bash

fileDiffArgs() {
  _ARGUMENTS=(
    [0]='file_a a "File A" true'
    [1]='file_b b "File B" true'
  )
}

fileDiff() {
  diff <(echo "${FILE_A}") <(echo "${FILE_B}")
}
