#!/usr/bin/env bash

portsOpened() {
  netstat -ntlp | grep LISTEN
}
