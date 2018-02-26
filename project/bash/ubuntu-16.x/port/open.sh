#!/usr/bin/env bash

portOpenArgs() {
  _ARGUMENTS=(
    [0]='port_number p "Port number" true'
  )
}

portOpen() {
  ufw allow ${PORT_NUMBER}/tcp
}
