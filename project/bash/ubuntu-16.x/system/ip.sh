#!/usr/bin/env bash

systemIp() {
  # May have several IP's
  IPS=($(ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'))
  # Take the last one
  echo ${IPS[-1]}
}
