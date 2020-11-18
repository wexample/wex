#!/usr/bin/env bash

codeAnalyseArgs() {
  _DESCRIPTION="Run quality tools a produce various stats about application"
  _ARGUMENTS=(
    'name n "Configuration file name" true'
  )
}

codeAnalyse() {
  # Use sonar scanner.
  docker run -ti -v $(pwd):/usr/src newtmitch/sonar-scanner \
      -Dproject.settings=./sonarqube/${NAME}.properties
}