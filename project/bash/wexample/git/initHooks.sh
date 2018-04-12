#!/usr/bin/env bash

# We just append command on git hooks
# We don't check if hooks already exists.
gitInitHooks() {
  local PATH_HOOKS=${WEX_DIR_ROOT}samples/git/hooks/
  local HOOKS=$(ls ${PATH_HOOKS})

  # For each hook in wex sample folder.
  for HOOK in ${HOOKS[@]}
  do
    local COMMAND="\n# Wex hooks"
    COMMAND+="\n. "${WEX_DIR_BASH}"wex false"
    COMMAND+="\n. "${PATH_HOOKS}${HOOK}
    local DIR_HOOKS=.git/hooks/
    local DEST=${DIR_HOOKS}${HOOK}

    if [ -f ${DEST} ];then
      # Append
      echo -e ${COMMAND} >> ${DEST}
    else
      # Create
      echo -e "#!/usr/bin/env bash\n"${COMMAND} > ${DEST}
    fi;
  done
}
