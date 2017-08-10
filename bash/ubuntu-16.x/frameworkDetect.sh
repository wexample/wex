#!/usr/bin/env bash

frameworkDetect() {
  websiteDir=./
  WEBSITE_FRAMEWORK="default"
  if [ ! -z "${1+x}" ] && [ ${1} != '' ] && [ ${1} != false ]; then
    websiteDir=${1}
  fi;

  # There is a composer folder, or any sign of a PHP framework.
  if [ -e ${websiteDir}"/composer.json" ] || [ -e ${websiteDir}"/index.php" ]
  then
    WEBSITE_FRAMEWORK=$(php "${WEX_DIR_BASH_UBUNTU16}../../php/websiteFolderFrameworkDetect.php" ${websiteDir});
  fi

  # PHP script found a framework name.
  echo ${WEBSITE_FRAMEWORK};
}
