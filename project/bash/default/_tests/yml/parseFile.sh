#!/usr/bin/env bash

ymlParseFileTest() {
  local filePath=$(wexTestSampleInit docker-compose.sample.yml)
  local parsed=$(wex yml/parseFile -f=${filePath})

  eval "${parsed}"

  wexTestAssertEqual "${services_network_phpmyadmin_environment_PMA_HOST}" "network_mysql"
}
