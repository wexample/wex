#!/usr/bin/env bash

gitHasChanges() {
    if [ -z "$(git status --porcelain)" ]; then
      echo false
    else
      echo true
    fi
}