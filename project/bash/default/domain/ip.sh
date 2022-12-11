#!/usr/bin/env bash

domainIpArgs() {
  _ARGUMENTS=(
    'domain d "Domain" true'
  )
}

domainIp() {
  ping -c 1 "${DOMAIN}" | grep "64 bytes from " | awk '{print $4}' | cut -d":" -f1
}
