#!/usr/bin/env bash

arrayContainsArgs() {
  _ARGUMENTS=(
    [0]='array a "Array content" true'
    [1]='item i "Item" true'
  )
}

arrayContains() {
  if [[ " ${ARRAY[@]} " =~ " ${ITEM} " ]]; then
    echo true
    return
  fi
  echo false
  return
}