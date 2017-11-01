#!/usr/bin/env bash

gitResetHard() {
  # Revert changes to modified files.
  git reset --hard
  # Remove all untracked files and directories.
  # (`-f` is `force`, `-d` is `remove directories`)
  git clean -fd
}
