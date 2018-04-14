#!/usr/bin/env bash

urlEncodeArgs() {
  _ARGUMENTS=(
    [0]='text t "Text to encode" true'
  )
}

urlEncode() {
  local strlen=${#TEXT}
  local encoded=""
  local pos c o

  for (( pos=0 ; pos<strlen ; pos++ )); do
     c=${TEXT:$pos:1}
     case "$c" in
        [-_.~a-zA-Z0-9] ) o="${c}" ;;
        * )               printf -v o '%%%02x' "'$c"
     esac
     encoded+="${o}"
  done
  echo "${encoded}"
}
