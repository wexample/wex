#!/usr/bin/env bash

portCloseArgs() {
  _ARGUMENTS=(
    [0]='port_number p "Port number" true'
  )
}

portClose() {
  ufw deny ${PORT_NUMBER}/tcp
}
