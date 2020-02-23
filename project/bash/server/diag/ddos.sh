#!/usr/bin/env bash

diagDdos() {
  # From : https://support.plesk.com/hc/en-us/articles/214529205-Apache-keeps-going-down-on-a-Plesk-server-server-reached-MaxRequestWorkers-setting
  # This command shows the list of source IP addresses and number of their current connections:
  netstat -an | egrep ':80|:443' | grep ESTABLISHED | awk '{print $5}' | grep -o -E "([0-9]{1,3}[\.]){3}[0-9]{1,3}" | sort -n | uniq -c | sort -nr
  # If the number of connections is high (400+) for some IP addresses, follow the steps from this KB article :
  # https://support.plesk.com/hc/en-us/articles/213390069
}