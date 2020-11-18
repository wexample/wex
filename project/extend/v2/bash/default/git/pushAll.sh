#!/usr/bin/env bash

gitPushAllArgs() {
  _ARGUMENTS=(
    [0]='message m "Commit message" true'
  )
}

gitPushAll() {
  # Git push again.
  git add .
  git commit -m "${MESSAGE}"
  git push -q
}