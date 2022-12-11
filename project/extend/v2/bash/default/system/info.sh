#!/usr/bin/env bash

systemInfo() {
  echo "OS :            "$(wex system/os)
  echo "Architecture :  "$(wex system/arch)
  echo "IP :            "$(wex system/ip)
  echo "Name :          "$(uname)
  echo "Hostname :      "$(uname -n)
  echo "Kernel v. :     "$(uname -v)
  echo "Kernel rel. :   "$(uname -r)
  echo "Machine :       "$(uname -m)
}
