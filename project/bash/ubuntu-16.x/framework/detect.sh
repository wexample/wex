#!/usr/bin/env bash

frameworkDetectArgs() {
  _ARGUMENTS=(
    [0]='dir d "Root directory of framework" false'
  )
}

# dependency : php, composer
frameworkDetect() {
  WEBSITE_FRAMEWORK=""

  if [[ -z "${DIR+x}" ]]; then
    # Get current dir.
    DIR=./
  fi;

  # There is a composer folder, or any sign of a PHP framework.
  if [[ -e ${DIR}"/composer.json" || -e ${DIR}"/index.php" ]]
  then
    WEBSITE_FRAMEWORK=$(php "${WEX_DIR_ROOT}php/websiteFolderFrameworkDetect.php" ${DIR});
  fi

  wex framework/global

  if [ "${WEX_FRAMEWORKS_SUPPORTED[${WEBSITE_FRAMEWORK}]}" == "" ];then
    echo "default"
  else
    # PHP script found a framework name.
    echo ${WEBSITE_FRAMEWORK};
  fi
}
