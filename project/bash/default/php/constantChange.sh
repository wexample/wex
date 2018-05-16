#!/usr/bin/env bash

phpConstantChangeArgs() {
 _ARGUMENTS=(
   [0]='key k "Key" true'
   [1]='value v "Value" true'
   [2]='file f "File" true'
 )
}

phpConstantChange() {
  sed -i "/"${KEY}"/s/'[^']*'/'"${VALUE}"'/2" ${FILE}
}