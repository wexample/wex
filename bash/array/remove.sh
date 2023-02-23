#!/usr/bin/env bash

arrayRemoveArgs() {
  _DESCRIPTION="Remove an item from a given array"
  # shellcheck disable=SC2034
  _ARGUMENTS=(
    'array a "Array content" true'
    'item i "Item value to remove" true'
  )
}

arrayRemove() {
  local OUTPUT=()

  for VALUE in ${ARRAY[@]}; do
    if [[ "${VALUE}" != "${ITEM}" ]]; then
      OUTPUT+=("${VALUE}")
    fi
  done

  echo "${OUTPUT[*]}"
}
