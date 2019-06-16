#!/usr/bin/env bash

sshPrintPubArgs() {
  _ARGUMENTS=(
    [0]='file f "Public key file" true'
  )
}

sshPrintPub() {
  # Convert a multi lines public file to a single line.
  echo "ssh-rsa "$(head -8 ${FILE} | tail -6 | tr -d '\n')
}
