#!/usr/bin/env bash

arraySortArgs() {
  _DESCRIPTION="Sort array values alphabetically"
  # shellcheck disable=SC2034
  _ARGUMENTS=(
    'array a "Array content" true'
    'separator s "Separator" false'
  )
}

arraySort() {
  local

  IFS=${SEPARATOR} read -r -a ARRAY_TEMP <<< "${ARRAY}"

  SORTED=($(printf "%s\n" "${ARRAY_TEMP[@]}" | sort))

  ARRAY=$(printf "${SEPARATOR}%s" "${SORTED[@]}")
  ARRAY="${ARRAY:1}"

  echo "$ARRAY"
}
