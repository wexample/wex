#!/usr/bin/env bash

onlyofficeConfig() {

  echo "\nSITE_CONTAINER=onlyoffice"

  . .wex

  echo "\nONLYOFFICE_DOCUMENT_SERVER_VERSION=${ONLYOFFICE_DOCUMENT_SERVER_VERSION}"

}
