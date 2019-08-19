#!/usr/bin/env bash

_wex_autocomplete() {
  local CUR=${COMP_WORDS[COMP_CWORD]}
  local WEX_DIR_BASH="/opt/wex/project/bash"
  local WEX_DIR_BASH_GROUPS=$(ls ${WEX_DIR_BASH})
  local SUGGESTIONS=();

  local SPLIT=($(wex text/split -t=${CUR} -s=/))
  local SEEK_GROUP=${SPLIT[0]}
  local SEEK_SCRIPT=${SPLIT[1]}
  local HAS_GROUP=$([ ${SEEK_GROUP} != ${CUR} ] && echo "true" || echo "false");

  local RED='\033[1;31m'
  local NC='\033[0m'

  # Search into extend directories.
  for WEX_DIR_BASH_GROUP in ${WEX_DIR_BASH_GROUPS[@]}
  do
    local WEX_GROUPS=$(ls ${WEX_DIR_BASH}/${WEX_DIR_BASH_GROUP});

    for BASH_GROUP in ${WEX_GROUPS[@]}
    do
      # This is a directory.
      local GROUP_DIR=${WEX_DIR_BASH}/${WEX_DIR_BASH_GROUP}/${BASH_GROUP}
      if [ -d ${GROUP_DIR} ];then

        # We search for a script file
        if [ ${HAS_GROUP} = true ];then
          local SCRIPTS=$(ls ${GROUP_DIR});

          # Iterate over scripts files.
          for SCRIPT in ${SCRIPTS[@]}
          do
            SUGGESTIONS+=" "$(basename ${BASH_GROUP})"/"$(echo ${SCRIPT} | cut -f 1 -d '.')
          done;
        # We search for a group folder.
        else
          SUGGESTIONS+=" "$(basename ${BASH_GROUP})"/"
        fi
      fi
    done;
  done;

  COMPREPLY=( $(compgen -W "${SUGGESTIONS}" -- ${CUR}) )
}

complete -o nospace -F _wex_autocomplete wex