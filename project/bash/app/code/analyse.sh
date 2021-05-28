#!/usr/bin/env bash

codeAnalyseArgs() {
  _DESCRIPTION="Run quality tools a produce various stats about application"
  _ARGUMENTS=(
    'name n "Configuration file name" false project'
  )
}

codeAnalyse() {
  # TODO use new version
  # https://docs.sonarqube.org/latest/analysis/scan/sonarscanner/
  #docker run \
  #    --rm \
  #    -e SONAR_HOST_URL="https://sonar.wexample.com" \
  #    -e SONAR_LOGIN="f298f259bcf263ca75f307ad9ef8cbcafc619669" \
  #    -v "${pwd}:/usr/src" \
  #    sonarsource/sonar-scanner-cli

  # Use sonar scanner.
  echo docker run -ti -v $(pwd):/usr/src newtmitch/sonar-scanner \
      -Dproject.settings=/usr/src/sonarqube/${NAME}.properties
}
