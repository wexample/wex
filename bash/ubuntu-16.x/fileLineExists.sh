#!/usr/bin/env bash

fileLineExists() {
  FILE=${1}
  LINE=${2}

  # Protect arguments by escaping special chars.
  LINE=$(sed -e 's/[]\/$*.^|[]/\\&/g' <<< "${LINE}")
  # Find line.
  results=$(sed -n "s/^\(${LINE}\)$/\1/p" ${FILE})

  if [ "${results}" != "" ]; then
    echo true
    return
  fi

  echo false
}

