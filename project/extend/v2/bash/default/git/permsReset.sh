#!/usr/bin/env bash

gitPermsReset() {
  git diff -p -R --no-color \
    | grep -E "^(diff|(old|new) mode)" --color=never  \
    | git apply
}
