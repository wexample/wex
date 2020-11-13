#!/usr/bin/env bash

portUsedArgs() {
  _ARGUMENTS=(
    [0]='port_number p "Port number" true'
  )
}

portUsed() {
  if lsof -Pi :${PORT_NUMBER} -sTCP:LISTEN -t >/dev/null ; then
    echo true
  else
    echo false
  fi
}
