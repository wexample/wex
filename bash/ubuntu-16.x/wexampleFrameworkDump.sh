#!/usr/bin/env bash

wexampleFrameworkDump() {
  # Wexample uses .env files on websites root to define variables
  # used globally by Docker and also available to define information about
  # data storage or containers connexion.

  # Load .env file
  . ".env"
  prefix=$(wexample frameworkGetEnvironment)"-"
  # Create dump
  dumpFile=$(wexample frameworkDump -s='./' -d=${VOLUME_DATA_DUMPS} -p=${prefix} -gz)
  # Create a symlink for the latest dump.
  ln -sf ${dumpFile} $(wexample wexampleFrameworkDumpLatestPath)".gz"
}
