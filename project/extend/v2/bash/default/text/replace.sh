#!/usr/bin/env bash

textReplaceArgs() {
  _ARGUMENTS=(
    [0]='text t "Text to work on" true'
    [1]='search s "Search" true'
    [2]='replace r "Replace" true'
  )
}

textReplace() {
  echo ${TEXT//${SEARCH}/${REPLACE}}  # The secret code is XXXXX
}