#!/usr/bin/env bash

wexampleFrameworkRestore() {
  # Wexample uses .env files on websites root to define variables
  # used globally by Docker and also available to define information about
  # data storage or containers connexion.

  # Choose between argument or latest dump.
  if [ ! -z "${1+x}" ]; then
    dumpFile=${1}
  else
    dumpFile=$(wexample wexampleFrameworkDumpLatestPath)".gz"
  fi;

  # Restore
  wexample frameworkRestore -s='./' -d=${dumpFile}
}
