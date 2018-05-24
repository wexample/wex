#!/usr/bin/env bash

portsOpenedArgs() {
  _ARGUMENTS=(
    [0]='separator s "Separator" false'
  )
}

portsOpened() {
  if [ -z "${SEPARATOR+x}" ];then
    # Default space separator
    SEPARATOR=" "
  fi;

  if [ $(wex docker/isToolBox) == true ];then
    return
  fi

  netstat -tuwanp4 | awk '{print $4}' | grep ':' | cut -d ":" -f 2 | sort | uniq | sed -e ':a' -e 'N' -e '$!ba' -e "s/\n/${SEPARATOR}/g"
}
