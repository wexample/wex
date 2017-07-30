#!/usr/bin/env bash

bashReadIfMissing() {
  variable_name=$1
  message=$2
  if [ -z ${variable_name+x} ]; then echo "var is unset"; else echo "var is set to '$var'"; fi
  read -p "${message} : " host
}
