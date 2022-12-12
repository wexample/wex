#!/usr/bin/env bash

autocomplete() {
  . /opt/wex/project/bash/globals.sh
  local CUR=${COMP_WORDS[${COMP_CWORD}]}
  local SUGGESTIONS=();
  local SPLIT=($(wex string/split -t="${CUR}" -s=/))
  local SEEK_GROUP=${SPLIT[0]}
  local SEEK_SCRIPT=${SPLIT[1]}
  local HAS_GROUP=$([ "${SEEK_GROUP}" != "" ] && [ ${SEEK_GROUP} != ${CUR} ] && echo "true" || echo "false");
  local WEX_SCRIPT_CALL_NAME=${COMP_WORDS[1]}
  local ARGS_INDEX=2;

  . "${WEX_DIR_BASH}includes/find-script-file.sh" "${CUR}"

  if [ "${COMP_WORDS[2]}" == "::" ];then
    ARGS_INDEX+=1
    local WEX_DIR_BASH_GROUPS=(${COMP_WORDS[1]})
  else
    if [ "${WEX_NAMESPACE_TEST}" != "" ];then
      local WEX_DIR_BASH_GROUPS=(${WEX_NAMESPACE_TEST} ${WEX_NAMESPACE_DEFAULT})
    else
      local WEX_DIR_BASH_GROUPS=(${WEX_NAMESPACE_DEFAULT})
    fi
  fi

  if (( ${COMP_CWORD} < ${ARGS_INDEX} ));then
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
  # Autocomplete args.
  else
    if [ ! -f "${WEX_SCRIPT_FILE}" ]; then
      return
    fi

    # Include found script file
    . "${WEX_SCRIPT_FILE}"

    ${WEX_SCRIPT_METHOD_ARGS_NAME}

    for ARG in "${_ARGUMENTS[@]}"
    do
       eval "SPLIT=(${ARG})"
       SUGGESTIONS+=" --"${SPLIT[0]}
    done
  fi

  COMPREPLY=( $(compgen -W "${SUGGESTIONS}" -- ${CUR}) )
}

autocomplete