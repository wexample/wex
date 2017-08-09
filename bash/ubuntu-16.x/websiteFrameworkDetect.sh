#!/usr/bin/env bash

websiteFrameworkDetect() {
  websiteDir=./
  WEBSITE_FRAMEWORK="undefined"
  if [ ! -z "${1+x}" ] && [ ${1} != '' ] && [ ${1} != false ]; then
    websiteDir=${1}
  fi;

  # There is a composer folder, or any sign of a PHP framework.
  if [ -e ${websiteDir}"/composer.json" ] || [ -e ${websiteDir}"/index.php" ]
  then

    eval $(php "${WEX_DIR_ROOT}../../php/websiteFolderFrameworkDetect.php" ${websiteDir});

    # PHP script found a framework name.
    if [ ${WEBSITE_FRAMEWORK} != "undefined" ]; then
      echo ${WEBSITE_FRAMEWORK};
      return
    fi
  fi
}
