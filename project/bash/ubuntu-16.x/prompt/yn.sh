#!/usr/bin/env bash

promptYnArgs() {
  _ARGUMENTS=(
    [0]='question q "Question to ask user" true'
  )
}

promptYn() {
  while true; do
    read -p "${QUESTION} [Y/n]: " yn
    case $yn in
        [Nn]* ) echo false; break;;
        * ) echo true; break;;
    esac
  done
}
