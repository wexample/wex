#!/usr/bin/env bash

domainFromUrlArgs() {
  _ARGUMENTS=(
    'url u "URL" true'
  )
}

domainFromUrl() {
  echo "${URL}" | awk -F/ '{print $3}'
}