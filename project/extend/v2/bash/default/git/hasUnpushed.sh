#!/usr/bin/env bash

gitHasUnpushed() {
    if [ -z "$(git cherry -v)" ]; then
      echo false
    else
      echo true
    fi
}