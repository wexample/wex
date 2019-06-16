#!/usr/bin/env bash

domainFromUrlArgs() {
  _ARGUMENTS=(
    [0]='url u "URL" true'
  )
}

domainFromUrl() {
  echo ${URL} | awk -F/ '{print $3}'
}