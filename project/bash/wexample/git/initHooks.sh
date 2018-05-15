#!/usr/bin/env bash

gitInitHooksArgs() {
 _ARGUMENTS=(
   [0]='recreate r "Remove previous files and recreate it" false'
 )
}

# We just append command on git hooks
# We don't check if hooks already exists.
gitInitHooks() {
  local PATH_GIT_HOOKS=.git/hooks/
  local GIT_HOOKS=$(ls ${PATH_GIT_HOOKS})
  local WEX_HOOK_CATCHER_NAME=wex-hook-catcher.sh
  local WEX_HOOK_CATCHER=${WEX_DIR_SAMPLES}git/${WEX_HOOK_CATCHER_NAME}

  # Copy hooks catcher
  cp -n ${WEX_HOOK_CATCHER} .git/hooks/

  for GIT_HOOK in ${GIT_HOOKS[@]}
  do
    if [ $(wex file/extension -f=${GIT_HOOK}) == sample ];then
      local NAME=$(wex file/name -f=${GIT_HOOK})
      local PATH_GIT_HOOK=${PATH_GIT_HOOKS}${NAME}
      local COMMAND="bash "${PATH_GIT_HOOKS}${WEX_HOOK_CATCHER_NAME}" "${NAME}" \${@}"

      if [ "${RECREATE}" == true ];then
        rm ${PATH_GIT_HOOK}
      fi

      if [ ! -f ${PATH_GIT_HOOK} ];then
        # Create file if missing.
        echo -e "#!/usr/bin/env bash" > ${PATH_GIT_HOOK}
      fi

      # Append once.
      wex file/textAppendOnce -f=${PATH_GIT_HOOK} -l="${COMMAND}"
      # Must be executable
      chmod +x ${PATH_GIT_HOOK}
    fi
  done
}
