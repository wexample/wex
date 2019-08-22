#!/usr/bin/env bash

shellClearArgs() {
  _DESCRIPTION='Simple command to clear the prompt content.'
}

shellClear() {
  printf "\033c"
}